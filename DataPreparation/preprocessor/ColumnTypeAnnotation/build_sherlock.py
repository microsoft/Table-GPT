import os
import pandas as pd
import numpy as np
import json
from collections import defaultdict

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def build_from_df(parse_fn, raw_df, save_dir, mode):
    count = 0
    count_test = 0
    for column_str, group_df in raw_df.groupby(by="column"):
        cand_set = sorted(set(group_df["ontology"].values))
        df = parse_fn(column_str)
        df = df.iloc[:30]
        count += 1
        df.to_csv(makedir([save_dir, f"{mode}{count}"], f"data.csv"), index=False)
        
        label = list(set(group_df[group_df["label"] == 1]["ontology"].values.tolist()))
        if len(label) == 0:
            label = None
        
        info = {
            "label": label,
            "candidates": cand_set
        }
        
        with open(makedir([save_dir, f"{mode}{count}"], f"info.json"), "w") as f:
            json.dump(info, f, indent=4)
        count_test += len(cand_set)

def parse_column_str_limaye(column_str):
    column = []
    for x in column_str.split(","):
        x_str = x.strip()
        if len(x_str) > 0:
            column.append(x_str)
    df = pd.DataFrame({"Column":column})
    return df

def build_sherlock(root_data_dir, root_save_dir):
    print("build CTA Sherlock")
    
    for mode in ["train", "test"]:
        if mode == "test":
            save_dir = os.path.join(root_save_dir, "test_only", "SherlockTest") 
            data = pd.read_parquet(os.path.join(root_data_dir, "Sherlock", f"test_values.parquet"))
            label = pd.read_parquet(os.path.join(root_data_dir, "Sherlock", f"test_labels.parquet"))
        else:
            save_dir = os.path.join(root_save_dir, "train_only", "SherlockTrain") 
            data = pd.read_parquet(os.path.join(root_data_dir, "Sherlock", f"train_values.parquet"))
            label = pd.read_parquet(os.path.join(root_data_dir, "Sherlock", f"train_labels.parquet"))

        candidates = sorted(set(label["type"].values))
        print(len(data), len(label))
        np.random.seed(1)
        # random sample 1000
        if mode == "train":
            sample_indices = np.random.permutation(len(data))[:10000]    
        else:
            sample_indices = np.random.permutation(len(data))[:1000]
            # sample_indices = range(len(data))
            # print(len(data))

        for i in sample_indices:
            raw = eval(data.iloc[i]["values"])
            value = [str(x) for x in raw if len(str(x))>0]
            y = label.iloc[i]["type"]
            
            df = pd.DataFrame({"Column": value})
            info = {
                "label": [y],
                "candidates": candidates
            }
            
            df.to_csv(makedir([save_dir, f"{mode}{i}"], f"data.csv"), index=False)
            with open(makedir([save_dir, f"{mode}{i}"], f"info.json"), "w") as f:
                json.dump(info, f, indent=4)
        
