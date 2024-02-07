import os
import pandas as pd
import utils
from collections import Counter

version = "v4"
data_dir = f"TrainTestDataFinal{version}/TrainData-FinalData-tokens_4096"
save_dir = f"VaryTrain{version}"

def count(data):
    tasks = [utils.parse_metadata(x)["task"] for x in data["metadata"].values]
    return Counter(tasks)

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
    
    # print("original distribution:", count(data))
    # print("perturb distributon:", count(add_df))
    return merge_df

sample_ratio = [0.025, 0.05, 0.1, 0.2, 0.4, 1]

jsonl_files = [os.path.join(data_dir, f) for f in sorted(os.listdir(data_dir))]
merge_data = utils.merge_shuffle_jsonl_files(jsonl_files, seed=1)

for s in sample_ratio:
    data, perturb_data = remove_perturb(merge_data)    
    size = int(len(data) * s)
    sample = data.iloc[:size]
    sample = add_perturb(sample, perturb_data)
    save_path = utils.makedir([save_dir], f"VaryTrain-TrainData-FinalData{version}-tokens_4096-PerturbSample_{s}-Size_{len(sample)}")
    save_path = save_path.replace(".", "_") + ".jsonl"
    utils.save_as_jsonl(sample, save_path)



