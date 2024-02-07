import numpy as np
import sys
import os
import jsonlines
import pandas as pd
import utils

def merge_jsonl_files(jsonl_files, merged_file_path, seed=1):
    data = []
    for path in jsonl_files:
        df = pd.read_json(path, lines=True)
        print(path, len(df))
        data.append(df)
    data = pd.concat(data, axis=0).reset_index(drop=True)
    data = data.sample(frac=1, random_state=seed)
    data.to_json(merged_file_path + f"-Size{len(data)}.jsonl", orient='records', lines=True)
    
data_dir = sys.argv[1].rstrip("/")

jsonl_files = []
for x in sorted(os.listdir(os.path.join(data_dir, "jsonl"))):
    if x.endswith(".jsonl"):
        jsonl_files.append(os.path.join(data_dir, "jsonl", x))

if len(sys.argv) > 2:
    save_path = utils.makedir([data_dir, "query"], f"{sys.argv[2]}")
else:
    save_path = utils.makedir([data_dir, "query"], f"{data_dir.strip('/').split('/')[-1].replace('.', '_')}")
merge_jsonl_files(jsonl_files, save_path, seed=1)