import pandas as pd
import os
import pandas as pd
import numpy as np
import json

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def get_random_fewshot_samples(n_samples, train_full, mv_column):
    fewshot = []
    for j in range(n_samples):
        df_sample = train_full.sample(n=1, random_state=j+2)
        test_row = df_sample.iloc[0:1]
        label = test_row[mv_column].values[0]
        mv_test_row = test_row.copy()
        mv_test_row[mv_column] = '[MISSING]'
        test_case = pd.concat([mv_test_row], axis=0).reset_index(drop=True)
        
        info = {
            "mv_column_name": mv_column,
            "mv_row_idx": len(test_case),
            "label": label
        }
        fewshot.append((test_case, info))
    return fewshot

def get_stanford_fewshot_samples(train_full, stanford_manual, mv_column):
    # few shot samples
    fewshot = []
    for j in range(len(stanford_manual)):
        test_row = stanford_manual.iloc[j:j+1]
        label = test_row[mv_column].values[0]
        mv_test_row = test_row.copy()
        mv_test_row[mv_column] = '[MISSING]'
        test_case = pd.concat([mv_test_row], axis=0).reset_index(drop=True)
        
        info = {
            "mv_column_name": mv_column,
            "mv_row_idx": len(test_case),
            "label": label
        }
        fewshot.append((test_case, info))
    return fewshot

def build_buy_restaurant_row_by_row(data_dir, dataset, root_save_dir):
    save_dir = os.path.join(root_save_dir, "test_only")
    train_full = pd.read_csv(os.path.join(data_dir, dataset, "train.csv"))
    test = pd.read_csv(os.path.join(data_dir, dataset, "test.csv"))
    stanford_manual = pd.read_csv(os.path.join(data_dir, dataset, "stanford_manual_fewshot.csv"))
    
    if dataset == "Buy":
        mv_column = "manufacturer"
    else:
        mv_column = "city"
    
    # few shot samples
    random_fewshot = get_random_fewshot_samples(10, train_full, mv_column)
    stanford_fewshot = get_stanford_fewshot_samples(train_full, stanford_manual, mv_column)

    for i in range(len(test)):
        test_row = test.iloc[i:i+1]
        label = test_row[mv_column].values[0]
        mv_test_row = test_row.copy()
        mv_test_row[mv_column] = '[MISSING]'
        
        test_case = pd.concat([mv_test_row], axis=0).reset_index(drop=True)
        test_case.to_csv(makedir([save_dir, f"{dataset}RowByRowTest", f"Table{i+1}"], "data.csv"), index=False)
    
        info = {
            "mv_column_name": mv_column,
            "mv_row_idx": len(test_case)-1,
            "label": label
        }

        with open(os.path.join(save_dir, f"{dataset}RowByRowTest", f"Table{i+1}", "info.json"), "w") as f:
            json.dump(info, f, indent=4)
        
        for j, (fewshot_test, fewshot_info) in enumerate(random_fewshot):
            fewshot_test.to_csv(makedir([save_dir, f"{dataset}RowByRowTest", f"Table{i+1}", "random_fewshot_samples", f"sample_{j}"], "data.csv"), index=False)
            with open(os.path.join(save_dir, f"{dataset}RowByRowTest", f"Table{i+1}", "random_fewshot_samples", f"sample_{j}", "info.json"), "w") as f:
                json.dump(fewshot_info, f, indent=4)
                
        for j, (fewshot_test, fewshot_info) in enumerate(stanford_fewshot):
            fewshot_test.to_csv(makedir([save_dir, f"{dataset}RowByRowTest", f"Table{i+1}", "stanford_fewshot_samples", f"sample_{j}"], "data.csv"), index=False)
            with open(os.path.join(save_dir, f"{dataset}RowByRowTest", f"Table{i+1}", "stanford_fewshot_samples", f"sample_{j}", "info.json"), "w") as f:
                json.dump(fewshot_info, f, indent=4)

