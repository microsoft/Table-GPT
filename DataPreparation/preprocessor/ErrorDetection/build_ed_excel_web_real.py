import pandas as pd
import numpy as np
import os
import json

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def parse_excel(x):
    x_list = eval(x)
    if len(x_list) == 0:
        return []
    else:
        return x_list[0]

def parse_web(x):
    x_list = eval(x)
    if len(x_list) == 0:
        return []
    else:
        return x_list

def preprocess(pos, neg, parse_fn):
    typo_pos = pos[pos["error_type"] == "Typo"]
    df = pd.concat([typo_pos, neg], axis=0).reset_index(drop=True)
    df["column_values"] = df["col-vals-for-benchmark"].apply(lambda x: eval(x))
    df["errors"] = df["error-pair"].apply(lambda x: parse_fn(x))
    return df

def get_data(row):
    values = np.array(row["column_values"]).reshape(-1, 1)
    columns = [row["col-name"]]
    data = pd.DataFrame(values, columns=columns)
    label = row["errors"]
    if len(label) == 0:
        label = None
    info = {
        "label": label
    }
    return data, info
    
    
def build_excel_web_real(data_dir, dataset, root_save_dir):
    print("build excel real")
    save_dir = os.path.join(root_save_dir, "test_only", dataset)
    pos = pd.read_csv(os.path.join(data_dir, dataset, "pos.csv"))
    neg = pd.read_csv(os.path.join(data_dir, dataset, "neg.csv"))
    pos_examples = pd.read_csv(os.path.join(data_dir, dataset, "pos_examples.csv"))
    neg_examples = pd.read_csv(os.path.join(data_dir, dataset, "neg_examples.csv"))
    
    if "Web" in dataset:
        parse_fn = parse_web
    elif "Excel" in dataset:
        parse_fn = parse_excel
    else:
        raise
    
    examples = preprocess(pos_examples, neg_examples, parse_fn)
    df = preprocess(pos, neg, parse_fn)
    
    count = 0
    num_except = 0
    for _, row in df.iterrows():
        count += 1
        data, info = get_data(row)
        data.to_csv(makedir([save_dir, f"Table{count}"], "data.csv"), index=False)
        with open(makedir([save_dir, f"Table{count}"], "info.json"), "w") as f:
            json.dump(info, f, indent=4)
        
        for j, ex_row in examples.iterrows():
            ex_data, ex_info = get_data(ex_row)
            ex_data.to_csv(makedir([save_dir, f"Table{count}", "random_fewshot_samples", f"sample_{j}"], "data.csv"), index=False)
            if ex_info["label"] is None:
                ex_info["correct_cell"] = None
            else:
                ex_info["correct_cell"] = [ex_info["label"][1]]
                ex_info["label"] = [ex_info["label"][0]]
            with open(makedir([save_dir, f"Table{count}", "random_fewshot_samples", f"sample_{j}"], "info.json"), "w") as f:
                json.dump(ex_info, f, indent=4)
            
    print("Except occured", num_except)