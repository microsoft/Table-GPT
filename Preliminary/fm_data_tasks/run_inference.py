"""Run inference."""
import argparse
import json
import logging
from pathlib import Path

import numpy as np
from manifest import Manifest

import fm_data_tasks.utils.data_utils as data_utils
import fm_data_tasks.utils.prompt_utils as prompt_utils
from fm_data_tasks.utils import constants
from fm_data_tasks.utils.utils import compute_metrics, setup_logger
import os
from collections import defaultdict
import pickle
from tqdm import tqdm
import pandas as pd
from copy import deepcopy
from time import sleep
from sklearn.metrics import precision_score, recall_score, f1_score
import openai
from transformers import GPT2TokenizerFast

with open("api_key.txt", "r") as f:
    openai_key = f.readlines()[0].strip("\n")
# os.environ["OPENAI_API_KEY"] = openai_key
os.environ["TOKENIZERS_PARALLELISM"] = "false"
openai.api_key = openai_key
logger = logging.getLogger(__name__)
MAX_TOKEN_LENGTH = 4096
result_logger = {}

def invoke_one_case_davinci_3(final_prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=final_prompt,
        temperature=0,
        max_tokens=3,
        top_p=1.0,
        # stop='\n\n',
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    prediction = response['choices'][0].text
    return prediction


def invoke_one_case_chat_turbo_35(final_prompt):
    response = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
        model = 'gpt-3.5-turbo',
        messages = [ # Change the prompt parameter to the messages parameter
            {'role': 'user', 'content': final_prompt}
        ],
        temperature=0,
        #max_tokens=100,
        top_p=1.0,
        stop='\n\n',
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    prediction = response['choices'][0].message.content
    return prediction

def invoke_one_case(prompt, model_name):
    if model_name == "3":
        pred = invoke_one_case_davinci_3(prompt)
    elif model_name == "3.5":
        pred = invoke_one_case_chat_turbo_35(prompt)
    else:
        print("Error: wrong model name {}".format(model_name))
        raise Exception("Wrong model name")
    # print("- Prompt:")
    # print(prompt)
    # print("- Pred:")
    # print(pred)
    # print("-----")
    return pred

def parse_args() -> argparse.Namespace:
    """Generate args."""
    parser = argparse.ArgumentParser(description="Simple calculator")
    parser.add_argument(
        "--root_dir",
        type=str,
        help="Which data directory to run.",
        # required=True,
        default="/datadrive/peng/TableGPT/Preliminary/fm_data_tasks/data/datasets/entity_matching/"
    )
    parser.add_argument("--benchmark", type=str, default="structured")
    parser.add_argument(
        "--output_dir", type=str, help="Output directory.", default="outputs"
    )
    parser.add_argument(
        "--cache_name",
        type=str,
        help="Manifest cache type.",
        default="sqlite",
        choices=["redis", "sqlite", "noop"],
    )
    parser.add_argument(
        "--cache_connection",
        type=str,
        help="Manifest cache connection string.",
        default="fm_data_tasks.sqlite",
    )
    parser.add_argument(
        "--client_name",
        type=str,
        help="Manifest client type.",
        default="openai",
        choices=["openai", "opt", "huggingface"],
    )
    parser.add_argument(
        "--client_connection",
        type=str,
        help="Manifest client connection string.",
        default=None,
    )
    parser.add_argument(
        "--tag",
        type=str,
        help="Tag for run saving.",
        default=None,
    )
    parser.add_argument(
        "--overwrite_cache",
        action="store_true",
        help="Overwrite sqlite cache of input/output results.",
    )
    parser.add_argument("--k", type=int, help="Number examples in prompt", default=10)
    parser.add_argument(
        "--sample_method",
        type=str,
        help="Example generation method",
        default="manual",
        choices=["random", "manual", "validation_clusters"],
    )
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument(
        "--class_balanced",
        help="Class balance training data. Good for classification tasks \
             with random prompts.",
        action="store_true",
    )
    parser.add_argument(
        "--sep_tok",
        type=str,
        help="Separate for attr: val pairs in row. Default is '.'.",
        default=".",
    )
    parser.add_argument(
        "--nan_tok",
        type=str,
        help="Token to represent nan entries. Default is 'nan'.",
        default="",
    )
    parser.add_argument(
        "--num_run",
        type=int,
        help="Number examples to run through model.",
        default=-1,
    )
    parser.add_argument(
        "--num_trials",
        type=int,
        help="Number trials to run. Results will be averaged with variance reported.",
        default=1,
    )
    parser.add_argument(
        "--num_print",
        type=int,
        help="Number example prompts to print.",
        default=200,
    )
    parser.add_argument(
        "--add_task_instruction",
        help="Add task instruction to the prompt before examples.",
        action="store_true",
    )
    parser.add_argument("--task_instruction_idx", type=int, default=0)
    parser.add_argument("--do_test", help="Run on test file.", action="store_true")
    parser.add_argument(
        "--dry_run", help="Dry run. Do not actually ping model.", action="store_true"
    )

    parser.add_argument(
        "--stop_token", help="Token to stop on for a given generated response", default="\n"
    )
    # Model args
    parser.add_argument("--temperature", type=float, help="Temperature.", default=0.0)
    parser.add_argument(
        "--max_tokens", type=int, help="Max tokens to generate.", default=3
    )
    parser.add_argument(
        "--datasets", nargs='+', default=None
    )
    parser.add_argument(
        "--save_dir", default="result0526"
    )
    parser.add_argument(
        "--model_name", default="3"
    )
    parser.add_argument(
        "--use_cache", action="store_true", default=False
    )

    args = parser.parse_args()
    return args
        
def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def main():
    """Run main method."""
    base_args = parse_args()
    base_args.overwrite_cache = True
    base_args.do_test = True
    assert(base_args.model_name in ["3", "3.5"])
    
    base_args.save_dir = "{}_{}_{}_{}_model{}".format(base_args.save_dir, base_args.benchmark, base_args.sample_method, base_args.k, base_args.model_name)
    
    if base_args.tag is not None:
        base_args.save_dir += "_" + base_args.tag
    
    if base_args.sample_method == "random":
        base_args.num_trials = 5
        base_args.class_balanced = True
    
    if base_args.k == 0:
        base_args.sample_method = "random"
        base_args.add_task_instruction = True
    
    if base_args.add_task_instruction:
        base_args.save_dir += "_instruct"

    if base_args.datasets is None:
        base_args.datasets = list(os.listdir(os.path.join(base_args.root_dir, base_args.benchmark)))
        # base_args.datasets = ["Beer", "Fodors-Zagats", "iTunes-Amazon", "Amazon-Google", "DBLP-ACM", "Walmart-Amazon", "DBLP-GoogleScholar"]
        
    for dataset in base_args.datasets:
        args = deepcopy(base_args)
        args.dataset = dataset
        run(args)
    
def run(args):
    args.data_dir = os.path.join(args.root_dir, args.benchmark, args.dataset)
    print("Processing", args.data_dir, ". Save to", args.save_dir)
    
    if args.num_trials < 1:
        raise ValueError("num_trials must be greater than 0.")
    # Get absolute path
    args.data_dir = str(Path(args.data_dir).resolve())
    # setup_logger(args.output_dir)
    # logger.info(json.dumps(vars(args), indent=4))

    # Will set seed for pandas
    np.random.seed(args.seed)

    test_file = "test" if args.do_test else "validation"

    # Read pandas DF datasets
    pd_data_files = data_utils.read_data(
        data_dir=args.data_dir,
        class_balanced=args.class_balanced,
        add_instruction=False,
        max_train_samples=-1,
        max_train_percent=-1,
        sep_tok=args.sep_tok,
        nan_tok=args.nan_tok,
    )
    if test_file not in pd_data_files:
        raise ValueError(f"Need {test_file} data")

    train_data = pd_data_files["train"]
    test_data = pd_data_files[test_file]
    
    task = constants.DATA2TASK[args.data_dir]
    # logger.info(f"Using {args.task_instruction_idx} instruction idx")
    task_instruction = constants.DATA2INSTRUCT[args.data_dir]
    num_run = args.num_run
    if args.num_run == -1:
        num_run = test_data.shape[0]
    num_run = min(num_run, test_data.shape[0])

    # logger.info(f"Train shape is {train_data.shape[0]}")
    # logger.info(f"Test shape is {test_data.shape[0]}")
    # logger.info(f"Running {num_run} examples for {args.num_trials} trials.")

    # Setup manifest
    # manifest = Manifest(
    #     cache_name=args.cache_name,
    #     cache_connection=args.cache_connection,
    #     client_name=args.client_name,
    #     client_connection=args.client_connection,
    #     stop_token=args.stop_token,
    #     temperature=args.temperature,
    #     max_tokens=args.max_tokens,
    #     top_p=1.0,
    #     n=1,
    # )
    if args.add_task_instruction:
        prompt = lambda x: f"{task_instruction} {x}"
    else:
        prompt = lambda x: f"{x}"

    # generate promots
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    for trial_num in range(args.num_trials):  
        # load_cache
        cache_path = makedir([args.save_dir, args.dataset, "trail_{}".format(trial_num + 1)], "cache.p")
        
        if not args.use_cache or not os.path.exists(cache_path):
            cache = {}
            saved_prefix = None
            shorter_prefix = None
            print("Trial", trial_num)
            np.random.seed(args.seed + trial_num)
            queries = []
            for _, row in test_data.iterrows():            
                serialized_r = row["text"]

                if args.sample_method == "manual":
                    prefix_exs = prompt_utils.get_manual_prompt(args.data_dir, row)
                elif args.sample_method == "validation_clusters":
                    if saved_prefix is None:
                        # logger.info("Generating validation cluster prompt
                        saved_prefix = prompt_utils.get_validation_prompt(
                            args.validation_path,
                            num_examples=args.k,
                            task=task,
                        )
                    prefix_exs = saved_prefix
                else:
                    if saved_prefix is None:
                        saved_prefix, saved_shorter_prefix = prompt_utils.get_random_prompt(
                            pd_data_files["train"], num_examples=args.k
                        )
                    prefix_exs = saved_prefix
                    shorter_prefix = saved_shorter_prefix
                
                query = prompt((prefix_exs + "\n" + serialized_r).strip())

                token_ids = tokenizer(query)['input_ids']
                if len(token_ids) > (MAX_TOKEN_LENGTH - 1000):
                    print("The query is too long!!!!!!", args.dataset)
                    return
                    # good_length = False
                    # if shorter_prefix is not None:
                    #     for prefix_exs in shorter_prefix[::-1]:
                    #         query = prompt((prefix_exs + "\n" + serialized_r).strip())
                    #         token_ids = tokenizer(query)['input_ids']
                    #         if len(token_ids) <= (MAX_TOKEN_LENGTH - 1000):
                    #             good_length = True
                    #             break
                    
                    # if not good_length:
                    #     print(shorter_prefix[0])
                    #     print(len(shorter_prefix[0]), len(shorter_prefix[1]))
                    #     print("The query is too long and no shorter prefix is available!!!!!!", args.dataset)
                    #     raise
            
                queries.append(query)
            
            cache["prompts"] = queries
            cache["label_str"] = test_data["label_str"].values
            cache["preds"] = [None for _ in queries]
            
            with open(cache_path, "wb") as f:
                pickle.dump(cache, f)

    if args.dry_run:
        return

    for trial_num in range(args.num_trials):  
        if os.path.exists(os.path.join(args.save_dir, args.dataset, "trail_{}".format(trial_num + 1), "metrics.json")):
            print("Skip trial {} that has been finished.".format(trial_num+1))
            continue
            
        cache_path = os.path.join(args.save_dir, args.dataset, "trail_{}".format(trial_num + 1), "cache.p")
        with open(cache_path, "rb") as f:
            cache = pickle.load(f)
    
        prompts = cache["prompts"][:num_run]
        gt = cache["label_str"][:num_run]
        preds = cache["preds"][:num_run]
        
        idx = 0
        pbar = tqdm(range(len(prompts)))
        
        # Run a few for printing -- they are cached
        for idx in range(len(prompts)):
            if preds[idx] is None:                
                while True:
                    try:
                        pred = invoke_one_case(prompts[idx], args.model_name)
                        break
                    except Exception as e:
                        print("Error occurs:", str(e))
                        sleep(3)
                preds[idx] = pred
                cache["preds"][idx] = pred
            pbar.update(1)
            
            # save cache every 10 queries
            if (idx % 10 == 0) or (idx == len(prompts) - 1):
                with open(cache_path, "wb") as f:
                    pickle.dump(cache, f)
            
        pbar.close()

        # Save trial predictions
        save_data = test_data.iloc[:num_run].copy(deep=True).reset_index()
        save_data["preds"] = preds
        save_data["prompt"] = prompts
        
        labels_int = [int("yes" in l.lower()) for l in save_data["label_str"]]
        preds_int = [int("yes" in l.lower()) for l in save_data["preds"]]
        
        save_data["label_int"] = labels_int
        save_data["preds_int"] = preds_int
        save_data["correct"] = (save_data["label_int"] == save_data["preds_int"]).astype(int)
        
        # new evaluation
        new_prec = precision_score(labels_int, preds_int)
        new_rec = recall_score(labels_int, preds_int)
        new_acc = save_data["correct"].mean()
        new_f1 = f1_score(labels_int, preds_int)
        
        new_trial_metrics = {}
        new_trial_metrics["rec"] = new_rec
        new_trial_metrics["prec"] = new_prec
        new_trial_metrics["acc"] = new_acc
        new_trial_metrics["f1"] = new_f1
        
        # save logging
        with open(makedir([args.save_dir, args.dataset, "trail_{}".format(trial_num + 1)], "log.p"), "wb") as f:
            pickle.dump(save_data, f)
        save_data.to_csv(os.path.join(args.save_dir, args.dataset, "trail_{}".format(trial_num + 1), "log.csv"), index=False)
        summary_save = save_data[[c for c in save_data.columns if c not in ["prompt", "preds"]]]
        summary_save.to_csv(os.path.join(args.save_dir, args.dataset, "trail_{}".format(trial_num + 1), "result.csv"), index=False)
        prompt_save = save_data[["prompt", "preds"]]
        prompt_save.to_csv(os.path.join(args.save_dir, args.dataset, "trail_{}".format(trial_num + 1), "prompt.csv"))
        trail_args = vars(args)
        
        json.dump(trail_args, open(makedir([args.save_dir, args.dataset, "trail_{}".format(trial_num + 1)], "params.json"), "w"), indent=4)
        json.dump(new_trial_metrics, open(makedir([args.save_dir, args.dataset, "trail_{}".format(trial_num + 1)], "metrics.json"), "w"), indent=4)

if __name__ == "__main__":
    main()
