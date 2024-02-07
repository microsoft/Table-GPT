import os
import pandas as pd
import utils
import numpy as np

version = "v4"

# task_group_1 = ["EntityMatching"]
# task_group_2 = ["EntityMatching", 
#                 "ErrorDetection", 
#                 "Row2RowFewshot", 
#                 "TableSummary", 
#                 "RowColumnSorting"]
# task_group_3 = ["EntityMatching", "SchemaMatching",
#                 "ErrorDetection", "DataImputation",
#                 "Row2RowFewshot", "ListExtraction", 
#                 "TableSummary", "RowGeneration",
#                 "RowColumnSorting", "RowColumnFiltering"]

def sample_tasks(i):
    taskset_1 = ["EntityMatching","SchemaMatching","HeaderValueMatching"]
    taskset_2 = ["ErrorDetection","DataImputation"]
    taskset_3 = ["Row2RowFewshot","ListExtraction","NL2SQL"]
    taskset_4 = ["TableSummary","RowGeneration","ColGeneration"]
    taskset_5 = ["RowColumnSwapping","RowColumnFiltering","RowColumnSorting"]
    tasksets = [taskset_1, taskset_2, taskset_3, taskset_4, taskset_5]

    seen = ["EntityMatching", "SchemaMatching", "ErrorDetection", "DataImputation", "Row2RowFewshot"]

    np.random.seed(i)
    task_group_1 = [seen[i]]
    task_group_2 = list(task_group_1)
    
    for ts in tasksets:
        if task_group_1[0] in ts:
            continue 
        task = np.random.choice(ts)
        task_group_2.append(task)

    task_group_3 = list(task_group_2)
    for ts in tasksets:
        remain = [task for task in ts if task not in task_group_2]
        task = np.random.choice(remain)
        task_group_3.append(task)
    
    return task_group_1, task_group_2, task_group_3
            


data_path = f"VaryTrain{version}/VaryTrain-TrainData-FinalDatav4-tokens_4096-PerturbSample_0_2-Size_17909.jsonl"
alias_df = pd.read_csv("task.csv")
alias = {}
for _, row in alias_df.iterrows():
    alias[row.Task] = row.Alias

def multitask_from_subset(seed):
    task_groups = sample_tasks(seed)
    save_dir = f"MultiTask{version}"
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
        name = f"MultiTask-TrainData-FinalData{version}-{len(task_group)}tasks-"
        name += "_".join([alias[t] for t in task_group])
        name += f"-Size_{len(subset)}"
        utils.save_as_jsonl(subset, utils.makedir([save_dir], name + ".jsonl"))
        
multitask_from_subset(1)
multitask_from_subset(2)
multitask_from_subset(3)
multitask_from_subset(4)