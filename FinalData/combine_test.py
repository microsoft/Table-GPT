import numpy as np
import sys
import os
import pandas as pd
import utils

# # entire 
version = "v4"

data_dir = f"TrainTestDataFinal{version}/TestData-FinalData-tokens_4096"
save_dir = utils.makedir([f"TrainTestDataFinalCombined{version}"])
files = [os.path.join(data_dir, f) for f in sorted(os.listdir(data_dir))]
merge_data = utils.merge_shuffle_jsonl_files(files, seed=None)
save_path = os.path.join(save_dir, f"TestData-FinalData{version}-tokens_4096-Size_{len(merge_data)}.jsonl")
utils.save_as_jsonl(merge_data, save_path)

def take_subset(selected_aliases, tag):
    files = []
    actual_aliases = []
    for f in sorted(os.listdir(data_dir)):
        alias = f[:-6].split("-")[-2]
        if alias in selected_aliases:
            actual_aliases.append(alias)
            files.append(os.path.join(data_dir, f))
    name = "_".join(actual_aliases)
    merge_data = utils.merge_shuffle_jsonl_files(files, seed=None)
    save_path = os.path.join(save_dir, f"TestData-FinalData{version}-tokens_4096-{tag}-{name}-Size_{len(merge_data)}.jsonl")
    utils.save_as_jsonl(merge_data, save_path)

# # Seen Exclude EM
task = pd.read_csv("task.csv")
task = task[task["Type"] != "TestOnly"]
task = task[task["Alias"] != "EM"]
selected_aliases = task["Alias"].values
take_subset(selected_aliases, tag="SeenExcludeEM")

# Unseen 
task = pd.read_csv("task.csv")
task = task[task["Type"] != "TrainTest"]
selected_aliases = task["Alias"].values
take_subset(selected_aliases, tag="Unseen")

# Unseen No CTA
task = pd.read_csv("task.csv")
task = task[task["Type"] != "TrainTest"]
task = task[task["Alias"] != "CTA"]
selected_aliases = task["Alias"].values
take_subset(selected_aliases, tag="UnseenExcludeCTA")

# ExcludeEM
task = pd.read_csv("task.csv")
task = task[task["Alias"] != "EM"]
selected_aliases = task["Alias"].values
take_subset(selected_aliases, tag="UnseenAndSeenExcludeEM")

task = pd.read_csv("task.csv")
selected_aliases = task["Alias"].values
take_subset(selected_aliases, tag="All")

task = pd.read_csv("task.csv")
selected_aliases = ["EM", "R2RF", "SM", "NS"]
take_subset(selected_aliases, tag="ExcludeSyn")
