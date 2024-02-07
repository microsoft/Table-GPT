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

def build_sqa(data_dir, root_save_dir):
    print("build SQA")
    error = 0
    for mode in ["train", "test"]:
        data = pd.read_csv(os.path.join(data_dir, "SQA", f"{mode}.tsv"), sep = '\t')
        data = data[data["position"] == 0]
        
        for _, row in data.iterrows():
            answer = eval(row["answer_text"])
            if len(answer) > 1:
                continue
            
            ans = answer[0]
            
            path = os.path.join(data_dir, "SQA", row["table_file"])
            df = pd.read_csv(path)
            
            if mode == "test":
                save_dir = makedir([root_save_dir, "test_only", "SQATest", f"table-{row['id']}-{row['annotator']}"])
            else:
                save_dir = makedir([root_save_dir, "train_only", "SQATrain", f"table-{row['id']}-{row['annotator']}"])
                                   
            df.to_csv(os.path.join(save_dir, "data.csv"), index=False)
            
            info = {
                "question": row["question"],
                "label": ans
            }
            
            with open(os.path.join(save_dir, "info.json"), "w") as f:
                json.dump(info, f, indent=4)
            
        print(mode, "Errors:", error)