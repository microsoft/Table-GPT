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


def remove_new_line(df_md):
    index = df_md.find('\n')
    df_md_clean = df_md[:index] + df_md[index+1:]
    return df_md_clean

def read_markdown_table(table_str: str) -> pd.DataFrame:
    df = pd.read_csv(StringIO(table_str), sep='|').dropna(axis=1, how='all').iloc[1:]
    return df

def clean(df_md):
    splits = df_md.split("|\n")
    clean = []
    for x in splits:
        clean.append(x.replace("\n", " "))
    return "|\n".join(clean)

def build_tq_wiki(data_dir, root_save_dir):
    print("build wikiTableQuestion")
    data = pd.read_csv(os.path.join(data_dir, "Wiki.csv"))
    error = 0

    for _, row in data.iterrows():
        df_id = row["id"]
        df_md = row["table_data_no_space"]
        df_md = clean(df_md)
        try:
            df = read_markdown_table(df_md)
        except:
            error += 1
            continue
        
        df.to_csv(makedir([root_save_dir, "test_only", "wiki", df_id], "data.csv"), index=False)
        
        info = {
            "question": row["utterance"],
            "label": row["targetValue"]
        }
        
        with open(os.path.join(root_save_dir, "test_only", "wiki", df_id, "info.json"), "w") as f:
            json.dump(info, f, indent=4)
        
    print("Errors:", error)