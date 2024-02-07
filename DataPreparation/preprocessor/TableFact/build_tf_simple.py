import pandas as pd
import os
import json
from io import StringIO
import re

def makedir(dir_list, file=None, replace=False):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def build_tf_simple(data_dir, root_save_dir):
    print("build TabFact")
    error = 0
    for mode in ["test", "train"]:
        if mode == "train":
            save_dir = os.path.join(root_save_dir, "train_only", "TabFactSimpleTrain")
        else:
            save_dir = os.path.join(root_save_dir, "test_only", "TabFactSimpleTest")
            
        with open(os.path.join(data_dir, f"TabFact_{mode}.json"), "r") as f:
            data = json.load(f)
            
        if mode == "test":
            with open(os.path.join(data_dir, "simple_test_id.json"), "r") as f_id:
                simple_ids = json.load(f_id)

        for table_id in data.keys():
            if mode == "test":
                if table_id not in simple_ids:
                    continue
                
            table = pd.read_csv(os.path.join(data_dir, "all_csv", table_id), sep="#")
            statement, labels, caption = data[table_id]
            assert(len(statement) == len(labels))
            
            for i, (s, y) in enumerate(zip(statement, labels)):
                info = {
                    "statement": s,
                    "label": y,
                    "caption": caption
                }
                
                with open(makedir([save_dir, f"{table_id[:-4]}-{i}"], "info.json"), "w") as ff:
                    json.dump(info, ff, indent=4)
                
                table.to_csv(makedir([save_dir, f"{table_id[:-4]}-{i}"], "data.csv"))