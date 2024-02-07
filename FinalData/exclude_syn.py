import os
import pandas as pd
import utils
import numpy as np

version = "v4"


data_path = f"VaryTrain{version}/VaryTrain-TrainData-FinalDatav4-tokens_4096-PerturbSample_0_2-Size_17909.jsonl"
alias_df = pd.read_csv("task.csv")
alias = {}
for _, row in alias_df.iterrows():
    alias[row.Task] = row.Alias

def multitask_from_subset():
    task_group = ["EntityMatching", "SchemaMatching", "Row2RowFewshot", "NL2SQL"]
    task_groups = [task_group]
    save_dir = f"ExcludeSyn{version}"
    data = pd.read_json(data_path, lines=True)
    data["task"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["task"])

    def take_subset(task_group):
        merge = []
        for task in task_group:
            subset = data[data["task"] == task]
            if len(subset) == 0:
                print(task)
                raise
            
            merge.append(subset)
        merge = pd.concat(merge, axis=0).reset_index(drop=True)
        merge = merge.sample(frac=1, random_state=1)
        return merge
    
    for task_group in task_groups:
        subset = take_subset(task_group)
        name = f"ExcludeSyn-TrainData-FinalData{version}-{len(task_group)}tasks-"
        name += "_".join([alias[t] for t in task_group])
        name += f"-Size_{len(subset)}"
        utils.save_as_jsonl(subset, utils.makedir([save_dir], name + ".jsonl"))
        
multitask_from_subset()
