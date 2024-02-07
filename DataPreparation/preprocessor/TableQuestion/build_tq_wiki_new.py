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

def build_tq_wiki(data_dir, root_save_dir):
    print("build wikiTableQuestion")
    error = 0
    for mode in ["train", "test"]:
        data = pd.read_csv(os.path.join(data_dir, "WikiTableQuestions", "data", f"{mode}.tsv"), sep = '\t')
        
        for _, row in data.iterrows():
            path = os.path.join(data_dir, "WikiTableQuestions", row["context"][:-3]+"tsv")
            
            try:
                df = pd.read_csv(path, sep = '\t')
            except:
                try:
                    df = pd.read_csv(path[:-3]+"csv")
                except:
                    error += 1
                    print(path)
                    continue
            
            if mode == "test":
                save_dir = makedir([root_save_dir, "test_only", "WikiTest", f"table-{row['id']}"])
            else:
                save_dir = makedir([root_save_dir, "train_only", "WikiTrain", f"table-{row['id']}"])
                                   
            df.to_csv(os.path.join(save_dir, "data.csv"), index=False)
            
            info = {
                "question": row["utterance"],
                "label": row["targetValue"]
            }
            
            with open(os.path.join(save_dir, "info.json"), "w") as f:
                json.dump(info, f, indent=4)
            
        print(mode, "Errors:", error)