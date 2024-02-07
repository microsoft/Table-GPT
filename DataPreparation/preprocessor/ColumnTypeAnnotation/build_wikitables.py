import json
import pandas as pd
import os
import numpy as np


def makedir(dir_list, file=None, replace=False):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def parse_table(value, header):
    num_rows = []
    for v in value:
        num_rows.append(max(x[0][0] for x in v) + 1)
    num_row = max(num_rows)
            
    df = [[None for j in range(len(value))] for i in range(num_row)]        

    for v in value:
        for x in v:
            i, j = x[0]
            df[i][j] = x[1][1]

    df = pd.DataFrame(df, columns=header)
    return df

def build_wikitables(root_data_dir, root_save_dir, max_train_size = None):
    candidates = []
    with open(os.path.join(root_data_dir, "WikiTables", "type_vocab.txt"), "r") as f:
        for line in f:
            cand = line.strip().split("\t")[1]
            candidates.append(cand)
            
    for mode in ["test", "train"]:
        with open(os.path.join(root_data_dir, "WikiTables", f"{mode}.table_col_type.json"), "r") as f:
            raw = json.load(f)
            
        if mode == "train":
            if max_train_size is not None and len(raw) > max_train_size:
                np.random.seed(1)
                indices = np.random.permutation(len(raw))[:max_train_size]
                raw = [raw[i] for i in indices]
        
        for _, row in enumerate(raw):
            row_id = str(row[0])
            header = row[5]
            value = row[6]
            df = parse_table(value, header)  
            labels = row[7]
            
            assert (len(labels) == df.shape[1])
            for i in range(df.shape[1]):
                df_i = df.iloc[:, i:i+1].dropna().iloc[:20]
                label = labels[i]
                
                info = {
                    "label": label,
                    "candidates": candidates,
                }
                df_i.to_csv(makedir([root_save_dir, f"{mode}_only", "WikiTables", f"{mode}_{row_id}_{i}"], "data.csv"), index=False)
                with open(makedir([root_save_dir, f"{mode}_only", "WikiTables", f"{mode}_{row_id}_{i}"], "info.json"), "w") as f:
                    json.dump(info, f, indent=4)