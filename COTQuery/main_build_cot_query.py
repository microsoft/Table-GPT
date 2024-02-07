import pandas as pd
import os
import argparse
import numpy as np
from datetime import date
from cot_query_generator.entity_matching.em_cot_query_generator import EMCOTQueryGenerator
from cot_query_generator.row2row_fewshot.r2rf_cot_query_generator import R2RFCOTQueryGenerator
from cot_query_generator.row_column_sorting.rcs_cot_query_generator import RCSCOTQueryGenerator
from cot_query_generator.row_column_swapping.rcsw_cot_query_generator import RCSWCOTQueryGenerator
from cot_query_generator.data_imputation.di_cot_query_generator import DICOTQueryGenerator
import json
import sys
sys.path.append("../Finetune")
import utils

def postprocess(data):
    # trim prompt ending, append completion
    new_data = []
    for _, row in data.iterrows(): 
        new_prompt = row["prompt"].rstrip() + "\n" + row["completion"].strip() + "\n\n"
        new_data.append({"prompt":new_prompt, "completion": row["completion"], "metadata":row["metadata"]})
    new_data = pd.DataFrame(new_data)
    return new_data
    

parser = argparse.ArgumentParser()
parser.add_argument("--root_dir", default="../Finetune/data")
parser.add_argument("--data_version", default="9.15")
parser.add_argument("--cot_data_dir", default="../COTQuery/data")
parser.add_argument("--task", nargs="+", default=None)
parser.add_argument("--mode", default="train", choices=["train", "test", "val"])
parser.add_argument("--serializer", default="markdownshort")
parser.add_argument("--tag", default=None)
parser.add_argument("--max_token_length", type=int, default=4096)
parser.add_argument("--max_size_per_dataset", type=int, default=500)
parser.add_argument("--seed", type=int, default=1)
parser.add_argument("--n_jobs", type=int, default=-1)
parser.add_argument("--debug", action="store_true", default=False)
parser.add_argument("--verbose", action="store_true", default=False)
args = parser.parse_args()

version = "7"
cot_query_version = f"{args.data_version}.{version}"

if args.n_jobs < 0:
    args.n_jobs = os.cpu_count()
    
args.result_dir = os.path.join("data", f"cot_data_v{cot_query_version}", "query_data")

for task in args.task:
    save_dir = utils.makedir([args.result_dir, args.mode])
    debug_dir = utils.makedir([save_dir, "debug", task]) if args.debug else None

    if task == "r2rf":
        max_num_datasets = 5000
    else:
        max_num_datasets = None

    params = {
        "serializer": args.serializer,
        "num_few_shot_trials": 0,
        "max_token_length": args.max_token_length,
        "num_col_perturb": 0,
        "prob_train_few_shot": 0,
        "max_train_size": args.max_size_per_dataset,
        "random_state": args.seed,
        "debug_dir": debug_dir,
        "verbose": args.verbose,
        "n_jobs": args.n_jobs,
        "use_random_description": False,
        "use_random_template": False,
        "use_cot": False,
        "cot_data_dir": None,
        "cot_position": None,
        "max_num_datasets": max_num_datasets,
        "use_system_message": False
    }

    if task == "em":
        params["num_few_shot_samples"] = 0
        params["task"] = "EntityMatching"
        data_generator = EMCOTQueryGenerator(**params)
    elif task == "r2rf":
        params["num_few_shot_samples"] = 0
        params["task"] =  "Row2RowFewshot"
        data_generator = R2RFCOTQueryGenerator(**params)
    elif task == "rcs":
        params["num_few_shot_samples"] = 0
        params["task"] =  "RowColumnSorting"
        data_generator = RCSCOTQueryGenerator(**params)
    elif task == "rcsw":
        params["num_few_shot_samples"] = 0
        params["task"] =  "RowColumnSwapping"
        data_generator = RCSWCOTQueryGenerator(**params)
    elif task == "di":
        params["num_few_shot_samples"] = 0
        params["task"] =  "DataImputation"
        data_generator = DICOTQueryGenerator(**params)
    
    root_data_dir = os.path.join(args.root_dir, f"data_v{args.data_version}")
    data, invalid_data = data_generator.generate_data(root_data_dir, mode=args.mode)

    # trim prompt ending, append completion
    data = postprocess(data)
    
    # save data
    save_name = f"cot_query_data_{args.mode}_{args.max_token_length}_v{cot_query_version}-{task}"
    jsonl_save_dir = utils.makedir([save_dir, "jsonl"], f"{save_name}.jsonl")
    params_save_dir = utils.makedir([save_dir, "params"], f"{save_name}.json")
    params["data_size"] = len(data)
    params["invalid_data_size"] = len(invalid_data)
    json.dump(params, open(params_save_dir, "w"), indent=4)
    if len(invalid_data) > 0:
        invalid_save_dir = utils.makedir([save_dir, "invalid"], f"{save_name}.csv")
        invalid_data.to_csv(invalid_save_dir, index=False)

    data.to_csv(utils.makedir([save_dir, "csv"], f"{save_name}.csv"), index=False)

    if args.mode == "train":
        # shuffle train data
        data = data.sample(frac=1, random_state=args.seed)
        data[["prompt", "completion", "metadata"]].to_json(jsonl_save_dir, orient='records', lines=True)
    else:
        data[["prompt", "metadata"]].to_json(jsonl_save_dir, orient='records', lines=True)