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

def build_limaye(root_data_dir, root_save_dir):
    print("build CTA Limaye")
    dataset = "Limaye"
    for mode in ["train", "test"]:
        if mode == "train":
            save_dir = os.path.join(root_save_dir, "train_only", "LimayeTrain")
        else:
            save_dir = os.path.join(root_save_dir, "test_only", "LimayeTest") 
    
        with open(os.path.join(root_data_dir, dataset, f"{mode}.json"), "r") as f:
            raw = json.load(f)
        
        raw_df = pd.DataFrame(raw, columns=["column", "ontology", "label"])
        build_from_df(parse_column_str_limaye, raw_df, save_dir, mode)
        
def parse_column_str_t2d(column_str):
    column_header, column_value = column_str.split("[VAL]")     
    column_header = column_header.split("[ATT]")[1].strip()
    if len(column_header) == 0:
        column_header = "Column"
    column = []
    for x in column_value.strip().split(","):
        x_str = x.strip()
        if len(x_str) > 0:
            column.append(x_str)    
    df = pd.DataFrame({column_header:column})
    return df

def parse_column_str_eft(column_str):
    if column_str[:5] == "[VAL]":
        _, column_header, column_value = column_str.split("[VAL]")     
    else:
        column_header, column_value = column_str.split("[VAL]")     
        column_header = column_header.split("[ATT]")[1].strip()
    if len(column_header) == 0:
        column_header = "Column"
    column = []
    for x in column_value.strip().split(","):
        x_str = x.strip()
        if len(x_str) > 0:
            column.append(x_str)    
    df = pd.DataFrame({column_header:column})
    return df

def build_t2d(root_data_dir, root_save_dir):
    print("build CTA T2D")
    dataset = "T2D"
    for mode in ["train", "test"]:
        if mode == "train":
            save_dir = os.path.join(root_save_dir, "train_only", "T2DTrain")
        else:
            save_dir = os.path.join(root_save_dir, "test_only", "T2DTest") 
            
        with open(os.path.join(root_data_dir, dataset, f"{mode}.json"), "r") as f:
            raw = json.load(f)
        
        raw_df = pd.DataFrame(raw, columns=["column", "ontology", "label"])
        build_from_df(parse_column_str_t2d, raw_df, save_dir, mode)

def build_efthymiou(root_data_dir, root_save_dir):
    print("build CTA efthymiou")
    dataset = "efthymiou"
    for mode in ["train", "test"]:
        if mode == "train":
            save_dir = os.path.join(root_save_dir, "train_only", "EfthymiouTrain")
        else:
            save_dir = os.path.join(root_save_dir, "test_only", "EfthymiouTest") 
            
        with open(os.path.join(root_data_dir, dataset, f"{mode}.json"), "r") as f:
            raw = json.load(f)
        
        raw_df = pd.DataFrame(raw, columns=["column", "ontology", "label"])
        build_from_df(parse_column_str_eft, raw_df, save_dir, mode)
        
        