import os
import pandas as pd
import pickle
from tqdm import tqdm
import numpy as np
import json

def read_csv(path):
    df = pd.read_csv(path)
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
    return df

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def build_synthetic_sm(root_data_dir, dataset, root_save_dir):
    print("build Synthetic SM", dataset)
    data_dir = os.path.join(root_data_dir, "SyntheticSM", "data")
    cache_path = os.path.join(root_data_dir, "SyntheticSM/alter_headers", dataset, "cache.p")
    if dataset == "Web":
        save_dir = os.path.join(root_save_dir, "train_only", dataset)
    else:
        save_dir = os.path.join(root_save_dir, "test_only", dataset)
    
    with open(cache_path, "rb") as f:
        cache = pickle.load(f)
        cache = pd.DataFrame(cache).set_index("filenames")

    file_list = sorted(os.listdir(os.path.join(data_dir, dataset)))
    count = 0
    
    for i in tqdm(range(len(file_list))):
        file = file_list[i]
        row = cache.loc[file]
        pred = row.preds
        
        if pred is None:
            continue
        
        df = read_csv(os.path.join(data_dir, dataset, file))
        
        old_columns = list(df.columns)
        alter_columns = row.alter_headers

        if alter_columns is not None and len(old_columns) == len(alter_columns):
            count += 1
            alter_columns = [c.strip() for c in row.alter_headers]
            
            info = {
                "old_headers": old_columns,
                "alternative_headers": alter_columns
            }
            
            np.random.seed(count)
            shuffle = np.random.permutation(len(df))
            indices1 = shuffle[:len(df) // 2]
            indices2 = shuffle[len(df) // 2:]
            
            table_1 = df.iloc[indices1]
            table_2 = df.iloc[indices2]
            table_2.columns = alter_columns
            
            # randomly drop columns
            n_drop_1 = np.random.randint(0, 4)
            table_1 = table_1.sample(n=table_1.shape[1] - n_drop_1, axis=1)
            n_drop_2 = np.random.randint(0, 4)
            table_2 = table_2.sample(n=table_2.shape[1] - n_drop_2, axis=1)
            
            table_1 = table_1.iloc[:5]
            table_2 = table_2.iloc[:5]
            
            table_1.to_csv(makedir([save_dir, f"Table{count}"], "table1.csv"), index=False)
            table_2.to_csv(makedir([save_dir, f"Table{count}"], "table2.csv"), index=False)
            df.to_csv(makedir([save_dir, f"Table{count}"], "original.csv"), index=False)
            
            with open(makedir([save_dir, f"Table{count}"], "info.json"), "w") as f:
                json.dump(info, f, indent=4)