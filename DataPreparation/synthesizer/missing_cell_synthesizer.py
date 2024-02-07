import pandas as pd
import os
import numpy as np
from copy import deepcopy
import json
from tqdm import tqdm
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer

def inject_mv(df, random_state, mv_token="[MISSING]", mv_col_idx=None):
    np.random.seed(random_state)
    if mv_col_idx is None:
        cand_columns = [(i, c) for i, c in enumerate(df.columns)]
        idx =  np.random.choice(len(cand_columns))
        col_idx, col_name = cand_columns[idx]
    else:
        col_idx = mv_col_idx
        col_name = df.columns[col_idx]
    
    row_idx = np.random.choice(len(df))
    df_values = deepcopy(df.values)
    label = deepcopy(df_values[row_idx, col_idx])
    df_values[row_idx, col_idx] = mv_token
    df_mv = pd.DataFrame(df_values, columns=df.columns)
    return df_mv, col_name, row_idx, col_idx, label

class MissingCellSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "MissingCell"
        
    def synthesize_one(self, df_full, random_state, save_dir):
        df = df_full.iloc[:5]
        df_mv, col_name, row_idx, col_idx, label = inject_mv(df, random_state)
        info = {
            "mv_column_name": col_name,
            "mv_row_idx": row_idx,
            "mv_col_idx": col_idx,
            "label": label,
        }
        df_full.to_csv(makedir([save_dir], "gt.csv"), index=False)
        df_mv.to_csv(makedir([save_dir], "data.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)
            
        # few shot samples
        df_fewshot = df_full.iloc[5:]

        for j in range(10):
            df_sample = df_fewshot.sample(n=5, random_state=random_state+j+1)
            df_mv, col_name, row_idx, col_idx, label = inject_mv(df_sample, random_state+j+1, mv_col_idx=None)
            info = {
                "mv_column_name": col_name,
                "mv_row_idx": row_idx,
                "mv_col_idx": col_idx,
                "label": label,
            }
            df_sample.to_csv(makedir([save_dir, "random_fewshot_samples", f"sample_{j}"],  "gt.csv"), index=False)
            df_mv.to_csv(makedir([save_dir, "random_fewshot_samples", f"sample_{j}"], "data.csv"), index=False)
            with open(makedir([save_dir, "random_fewshot_samples", f"sample_{j}"], "info.json"), "w") as f:
                json.dump(info, f, indent=4)