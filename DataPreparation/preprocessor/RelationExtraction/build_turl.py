import json
import pandas as pd
import os

def makedir(dir_list, file=None, replace=False):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def parse_table(value, header):
    num_rows = []
    for v in value:
        num_rows.append(max(x[0][0] for x in v) + 1)
    num_row = max(num_rows)
            
    df = [[None for j in range(len(value))] for i in range(num_row)]        

    for v in value:
        for x in v:
            i, j = x[0]
            df[i][j] = x[1][1]

    df = pd.DataFrame(df, columns=header)
    return df

def build_turl(root_data_dir, root_save_dir):
    
    candidates = []
    with open(os.path.join(root_data_dir, "turl", "relation_vocab.txt"), "r") as f:
        for line in f:
            cand = line.strip().split("\t")[1]
            candidates.append(cand)
            
    for mode in ["test", "train"]:
        with open(os.path.join(root_data_dir, "turl", f"{mode}.json"), "r") as f:
            raw = json.load(f)
        
        
        for _, row in enumerate(raw):
            row_id = str(row[0])
            page_title = row[1]
            table_title = row[3]
            header = row[5]
            value = row[6]
            df = parse_table(value, header)
            df = df.dropna(how="all", axis=0)
            df = df.iloc[:20]
            
            labels = row[7]
            assert len(labels) == df.shape[1] - 1
            
            for i in range(df.shape[1] - 1):
                col_indices = [0, i+1]
                df_i = df.iloc[:, col_indices]
                label = labels[i]
                
                info = {
                    "label": label,
                    "candidates": candidates,
                    "page_title": page_title,
                    "table_title": table_title
                }
                df_i.to_csv(makedir([root_save_dir, f"{mode}_only", "turl", f"{mode}_{row_id}_{i}"], "data.csv"), index=False)
                with open(makedir([root_save_dir, f"{mode}_only", "turl", f"{mode}_{row_id}_{i}"], "info.json"), "w") as f:
                    json.dump(info, f, indent=4)