import pandas as pd
import os
import json
from tqdm import tqdm
import sys
sys.path.append("../..")
from utils import makedir
import numpy as np
from copy import deepcopy


def build_tde_wiki(data_dir, dataset, root_save_dir):
    print("build row2row", dataset)
    
    if dataset == "Wiki":
        mode = "train"
    elif dataset == "TDE":
        mode = "test_only"
    else:
        raise
    
    file_list = sorted(os.listdir(os.path.join(data_dir, dataset)))
    np.random.seed(1)
    count = 0
    for i in tqdm(range(len(file_list))):
        file = file_list[i]
        df = pd.read_csv(os.path.join(data_dir, dataset, file, "data.csv"))
        with open(os.path.join(data_dir, dataset, file, "info.json"), "r") as f:
            data_info = json.load(f)
        
        instruction = data_info["instruction"]
        df = df.astype(str)
        df = df.iloc[:10]
        data = deepcopy(df)
        
        if mode == "train":
            n_example = np.random.randint(1, 4)
        else:
            n_example = len(df) - 3
        
        data.iloc[-n_example:, 1] = None
        
        full_index = list(range(len(data) - n_example))
        
        for j in range(n_example):
            index = len(full_index) + j
            df_index = full_index + [index]
            data_i = data.iloc[df_index]
            gt_i = str(df["Output"].values[index])
            
            info = {
                "filename": file,
                "n_examples": 1,
                "label": gt_i,
                "instruction": instruction
            }
 
            data_i.to_csv(makedir([root_save_dir, mode, dataset, f"{file}_{j}"], "data.csv"), index=False)
            df.to_csv(makedir([root_save_dir, mode, dataset, f"{file}_{j}"], "origin.csv"), index=False)
            with open(makedir([root_save_dir, mode, dataset, f"{file}_{j}"], "info.json"), "w") as f:
                json.dump(info, f, indent=4)
                
