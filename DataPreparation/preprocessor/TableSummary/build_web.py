import pickle
import os
from tqdm import tqdm
import pandas as pd
import json

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def read_csv(path):
    df = pd.read_csv(path)
    df = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
    return df

def contains_unicode(x):
    for c in str(x):
        if ord(c) > 127:
            return True
    return False

def check_unicode_df(df):
    for column in df.columns:
        if df[column].apply(contains_unicode).any():
            return False
    return True

def build_ts_web(root_data_dir, root_save_dir):
    print("build table summary web")
    cache_path = os.path.join(root_data_dir, "web_summary.p")
    data_dir = os.path.join(root_data_dir, "Web")

    save_dir = os.path.join(root_save_dir, "train_only", "Web")
    
    file_list = sorted(os.listdir(data_dir))

    with open(cache_path, "rb") as f:
        summary = pickle.load(f)

    count = 0
    for i in tqdm(range(len(file_list))):
        file = file_list[i]
        name = file[:-4]
        
        if name not in summary:
            continue
        
        summ = summary[name]
        raw_key_words = summ.split("___")[1].split("-")
        key_words = [w.strip() for w in raw_key_words if len(w.strip()) > 0]
        
        if len(key_words) > 1:
            df = read_csv(os.path.join(data_dir, file))
            if not check_unicode_df(df):
                continue
            
            label = key_words[-1]
            
            # remove if token length < 3
            if len(label.split()) < 3:
                continue
            
            info = {
                "label": label,
                "keywords": key_words,
            }
            
            count += 1
            df.to_csv(makedir([save_dir, f"Table{count}"], "data.csv"), index=False)
            with open(makedir([save_dir, f"Table{count}"], "info.json"), "w") as f:
                json.dump(info, f, indent=4)