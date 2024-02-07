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
    return pred

def parse_args() -> argparse.Namespace:
    """Generate args."""
    parser = argparse.ArgumentParser(description="Simple calculator")
    parser.add_argument(
        "--root_dir",
        type=str,
        help="Which data directory to run.",
        # required=True,
        default="/datadrive/peng/TableGPT/Preliminary/fm_data_tasks/data/datasets/"
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
    parser.add_argument("--seed", type=int, default=1)
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
        default=3,
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
        "--result_dir", default="test_data_2048_0602"
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

def generate_test_ids(test_data, benchmark, dataset, sample_method, k, trial_num):
    test_ids = []
    for label, lrid in test_data[["label", "lrid"]].values:
        key = f"benchmark_{benchmark}___dataset_{dataset}___sampleMethod_{sample_method}___numSamples_{k}___trial_{trial_num}___id_{lrid}___label_{label}"
        test_ids.append(key)
    return test_ids

def main():
    """Run main method."""
    base_args = parse_args()
    base_args.overwrite_cache = True
    base_args.do_test = True
    assert(base_args.model_name in ["3", "3.5"])
    
    if base_args.sample_method == "random":
        base_args.class_balanced = True
    
    if base_args.k == 0:
        base_args.num_trials = 1
        base_args.sample_method = "random"
        base_args.add_task_instruction = True
    
    if base_args.sample_method == "manual":
        base_args.num_trials = 1
    
    if base_args.datasets is None:
        base_args.datasets = list(os.listdir(os.path.join(base_args.root_dir, base_args.benchmark)))
        # base_args.datasets = ["Beer", "Fodors-Zagats", "iTunes-Amazon", "Amazon-Google", "DBLP-ACM", "Walmart-Amazon", "DBLP-GoogleScholar"]

    test_data = []
    for dataset in base_args.datasets:
        for trial_num in range(base_args.num_trials):
            print("processing", dataset, "trial", trial_num)
            args = deepcopy(base_args)
            args.dataset = dataset
            args.trial_num = trial_num
            test_df = run(args)
            test_df["dataset_name"] = dataset
            # test_df["metadata"] = generate_test_ids(test_df, "stanford", dataset, args.sample_method, args.k, trial_num)
            test_data.append(test_df)
        
    test_data = pd.concat(test_data, axis=0).reset_index(drop=True)
    
    save_name = f"test_stanford_{base_args.benchmark}_{base_args.sample_method}_{args.k}"
    jsonl_save_dir = makedir([base_args.result_dir, save_name], "test_data.jsonl")
    csv_save_dir = makedir([base_args.result_dir, save_name], "test_data.csv")
    params_save_dir = makedir([base_args.result_dir, save_name], "params.json")

    args_dict = vars(base_args)
    json.dump(args_dict, open(params_save_dir, "w"), indent=4)
    test_data.to_csv(csv_save_dir, index=False)
    # test_data[["prompt", "completion", "metadata"]].to_json(jsonl_save_dir, orient='records', lines=True)
    test_data[["prompt", "completion"]].to_json(jsonl_save_dir, orient='records', lines=True)

    # lrid,prompt,completion,label,is_shorted,dataset_name,trial_num,metadata
    
def run(args):
    args.data_dir = os.path.join(args.root_dir, args.benchmark, args.dataset)
    args.data_dir = str(Path(args.data_dir).resolve())
    
    test_file = "test" if args.do_test else "validation"
    np.random.seed(args.seed)

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

    if args.add_task_instruction:
        prompt = lambda x: f"{task_instruction} {x}"
    else:
        prompt = lambda x: f"{x}"

    # generate promots
    queries = []
    saved_prefix = None
    np.random.seed(args.seed + args.trial_num)
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
                saved_prefix = prompt_utils.get_random_prompt(
                    pd_data_files["train"], num_examples=args.k
                )
            prefix_exs = saved_prefix
        
        query = prompt((prefix_exs + "\n" + serialized_r).strip())
        queries.append(query)
    
    test_df = {}
    # test_df["lrid"] = [f"{l}-{r}" for l, r in test_data[["id_A", "id_B"]].values]
    test_df["prompt"] = queries
    test_df["completion"] = [l.strip() for l in test_data["label_str"].values]
    # test_df["label"] = test_data["label"].values
    test_df["is_shorted"] = "Not shortened"
    test_df["trial_num"] = args.trial_num    
    test_df = pd.DataFrame(test_df)
    return test_df

if __name__ == "__main__":
    main()
