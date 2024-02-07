import pandas as pd
import sys
import argparse
import utils
from collections import Counter

def count(data):
    tasks = [utils.parse_metadata(x)["task"] for x in data["metadata"].values]
    return Counter(tasks)

def remove_ending(name):
    if "-Size" in name:
        prefix, suffix = name.split("-Size")
    else:
        prefix = name
    return prefix

def remove_perturb(data):
    non_perturb_mask = ["colPerturbSeed" not in x for x in data["metadata"].values]
    perturb_mask = ["colPerturbSeed" in x for x in data["metadata"].values]
    return data[non_perturb_mask], data[perturb_mask]

def get_key(metadata):
    parse = utils.parse_metadata(metadata)
    keys = ["task", "benchmark", "dataset", "sampleMethod", "numSamples", "seed"]
    if parse["task"] == "EntityMatching":
        keys.append("lrid")
    result = []
    for k in keys:
        result.append(f"{k}_{parse[k]}")
    return "___".join(result)
    
def add_perturb(data, perturb_data):
    perturb_index = {}
    for i, metadata in enumerate(perturb_data["metadata"].values):
        key = get_key(metadata)
        if key in perturb_index:
            print("Warning: duplicated key found", key)
        perturb_index[key] = i
        
    add_data_indices = []
    for metadata in data["metadata"].values:
        key = get_key(metadata)
        if key in perturb_index:
            add_data_indices.append(perturb_index[key])
            
    add_df = perturb_data.iloc[add_data_indices]    
    merge_df = pd.concat([data, add_df], axis=0).reset_index(drop=True)
    merge_df = merge_df.sample(frac=1, random_state=1)
    
    print("original distribution:", count(data))
    print("perturb distributon:", count(add_df))
    return merge_df
        
parser = argparse.ArgumentParser()
parser.add_argument("--data_path", default=None)
parser.add_argument("--sample", default=None, type=float, help="our sample rate")
parser.add_argument("--size", default=None, type=int)
parser.add_argument("--save_dir", default=None)
args = parser.parse_args()

full_data = pd.read_json(args.data_path, lines=True)
data, perturb_data = remove_perturb(full_data)

if args.size is not None:
    n_data = args.size
else:
    n_data = int(len(data) * args.sample)
    
data = data.iloc[:n_data]

data = add_perturb(data, perturb_data)
name = args.data_path.strip("/").split("/")[-1]
name = remove_ending(name)

if args.save_dir is not None:
    data.to_json(utils.makedir([args.save_dir], f"{name}_PerturbSample{args.sample}_Size{len(data)}".replace(".", "_") + ".jsonl", orient='records', lines=True))
else:
    data.to_json(f"{name}_PerturbSample_Sample{args.sample}_Size{len(data)}".replace(".", "_") + ".jsonl", orient='records', lines=True)

