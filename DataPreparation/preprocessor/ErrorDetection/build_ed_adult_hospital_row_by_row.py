import pandas as pd
import os
import pandas as pd
import numpy as np
import json
import sys
sys.path.append("../..")
from utils import makedir

def get_error_list(x):
    if pd.isna(x):
        return []
    else:
        return x.split("_____")

def get_clean_train(train):
    num_error = train["error_columns"].apply(lambda x: len(get_error_list(x)))
    clean_train = train[num_error == 0]
    dirty_train = train[num_error > 0]
    return clean_train, dirty_train

def build_adult_hospital_row_by_row(data_dir, dataset, root_save_dir):
    save_dir = os.path.join(root_save_dir, "test_only")
    print("build", dataset, "row by row")
    train = pd.read_csv(os.path.join(data_dir, dataset, "train.csv"))
    test = pd.read_csv(os.path.join(data_dir, dataset, "test.csv"))
    manual = pd.read_csv(os.path.join(data_dir, dataset, "manual.csv"))
    clean_train, dirty_train = get_clean_train(train)
    
    fewshot_samples = []
    for j in range(len(manual)):
        fewshot_clean_test = manual.iloc[j:j+1]
        fewshot = pd.concat([fewshot_clean_test], axis=0).reset_index(drop=True).drop(columns=["error_columns"])
        info = {
            "error_column_name": None,
            "error_row_idx": None,
            "label": None,
        }
        fewshot_samples.append((fewshot, info))
        
    for j in range(5):
        fewshot_dirty_test = dirty_train.sample(n=1, random_state=2+j)
        fewshot = pd.concat([fewshot_dirty_test], axis=0).reset_index(drop=True).drop(columns=["error_columns"])
        error = get_error_list(fewshot_dirty_test["error_columns"].values[0])
        
        if len(error) == 0:
            error = None
            label = None
            error_row_idx = None
        else:
            error_row_idx = len(fewshot) - 1
            label = [fewshot_dirty_test.iloc[0][x] for x in error]

        info = {
            "error_column_name": error,
            "error_row_idx": error_row_idx,
            "label": label,
        }
        fewshot_samples.append((fewshot, info))

            
    # task
    error_columns = test["error_columns"].apply(lambda x: get_error_list(x)).values
    test_table = test.drop(columns=["error_columns"])
 
    for i in range(len(test_table)):
        test_row = test_table.iloc[i:i+1]
        test_case = pd.concat([test_row], axis=0).reset_index(drop=True)
        
        error = error_columns[i]
        if len(error) == 0:
            error = None
            label = None
            error_row_idx = None
        else:
            error_row_idx = len(test_case) - 1
            label = [test_table.iloc[i][x] for x in error]

        info = {
            "error_column_name": error,
            "error_row_idx": error_row_idx,
            "label": label,
        }
        
        test_case.to_csv(makedir([save_dir, f"{dataset}RowbyRowTest", f"Table{i+1}"], "data.csv"), index=False)
        with open(os.path.join(save_dir, f"{dataset}RowbyRowTest", f"Table{i+1}", "info.json"), "w") as f:
            json.dump(info, f, indent=4)
            
        for j, (fewshot_test, fewshot_info) in enumerate(fewshot_samples):
            fewshot_test.to_csv(makedir([save_dir, f"{dataset}RowbyRowTest", f"Table{i+1}", "random_fewshot_samples", f"sample_{j}"], "data.csv"), index=False)
            with open(os.path.join(save_dir, f"{dataset}RowbyRowTest", f"Table{i+1}", "random_fewshot_samples", f"sample_{j}", "info.json"), "w") as f:
                json.dump(fewshot_info, f, indent=4)

