import pandas as pd
import os
import argparse
import numpy as np
from datetime import date
import pickle
from tqdm import tqdm
import sys
sys.path.append("../Finetune")
from gpt_api import GPT
import json
import utils
from collections import defaultdict

def load_test_data(data_dir):
    test_data = []
    for d in os.listdir(os.path.join(data_dir, "query")):
        df = pd.read_json(os.path.join(data_dir, "query", d), lines=True)
        test_data.append(df)
    test_data = pd.concat(test_data, axis=0).reset_index(drop=True)
    return test_data

def load_cache(cache_path, test_data):
    # load cache    
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            cache = pickle.load(f)
        for key in test_data["metadata"].values:
            if key not in cache:
                cache[key] = [None, None]
    else:
        cache = {key: [None, None] for key in test_data["metadata"].values}
        with open(cache_path, "wb") as f:
            pickle.dump(cache, f)
    return cache

def remove_prompt_ending(prompt):
    ending="\n\n###\n\n"
    if prompt.endswith(ending):
        prompt = prompt[:-len(ending)]
        prompt += "\n\n"
    return prompt
    
def run_tasks(cache, cache_path, api_keys, task_ids, test_data, model_name, max_tokens, n_jobs, batch_size):
    # process a batch of ids at every iteration
    batch_size = 64
    n_batches = (len(task_ids) - 1) // batch_size + 1
    gpt = GPT(api_keys=api_keys, model_name=utils.get_model_name(model_name), max_tokens=max_tokens, n_jobs=n_jobs)
            
    for i in tqdm(range(n_batches)):
        id_batch = task_ids[i*batch_size:(i+1)*batch_size]
        prompt_batch = [test_data.loc[idx]["prompt"] for idx in id_batch]

        result_batch = gpt.run_multi(prompt_batch)

        # save results
        for idx, (stat, pred) in zip(id_batch, result_batch):
            cache[idx] = [pred, stat]
        
        with open(cache_path, "wb") as f:
            pickle.dump(cache, f)
                
parser = argparse.ArgumentParser()
parser.add_argument("--data_dir", default="data")
parser.add_argument("--version", default=None)
parser.add_argument("--mode", default="train")
parser.add_argument("--model", default="D3")
parser.add_argument("--temperature", type=float, default=0.0)
parser.add_argument("--batch_size", type=int, default=64)
parser.add_argument("--n_jobs", type=int, default=8)
args = parser.parse_args()

max_tokens_map = defaultdict(lambda: 200)

api_keys = utils.load_api_keys("../Finetune/api_keys.txt")
args.n_jobs = min(args.n_jobs, len(api_keys))

data_dir = os.path.join(args.data_dir, f"cot_data_v{args.version}", "query_data", args.mode)

if not os.path.exists(data_dir):
    raise Exception(f"{data_dir} not exists")

test_data = load_test_data(data_dir)
cache_path = utils.makedir([data_dir, "cache"], f"{args.model}.p")
cache = load_cache(cache_path, test_data)
test_data["task"] = [utils.parse_metadata(meta)["task"] for meta in test_data["metadata"].values]
test_data = test_data.set_index("metadata")
test_data["prompt"] = test_data["prompt"].apply(remove_prompt_ending)

for task, test_data_group in test_data.groupby("task"):
    print("Running query for", task)
    task_ids = []
    for key, (pred, status) in cache.items():
        if key in test_data_group.index:
            if pred is None:
                task_ids.append(key)
                
    print("Number of queries:", len(task_ids))
    run_tasks(cache, cache_path, api_keys, task_ids, test_data, args.model, max_tokens_map[task], args.n_jobs, args.batch_size)


save_dir = os.path.join(utils.makedir([data_dir, "preds"], f"model{args.model}_vanilla.jsonl"))
preds_df = test_data.reset_index()
preds_df["choices"] = [[{"text": cache[idx][0]}] for idx in test_data.index]
preds_df["status"] = [cache[idx][1] for idx in test_data.index]
preds_df.to_json(save_dir, orient='records', lines=True)
