"""Extract tables from txt"""

import pandas as pd
import os
from collections import defaultdict
from tqdm import tqdm
import pickle

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

data_dir = "AllWikiCols.txt"

tables_dict = defaultdict(list)
count = 0
with open(data_dir, "r") as f:
    for line in f:
        columns = line.strip("\n").split("\t")
        table_id = columns[1]
        summary = columns[2]
        if table_id in tables_dict:
            continue

        tables_dict[table_id] = summary
with open("web_summary.p", "wb") as f:
    pickle.dump(tables_dict, f)
