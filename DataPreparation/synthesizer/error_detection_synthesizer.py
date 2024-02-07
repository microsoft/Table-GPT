import pandas as pd
import os
import numpy as np
from copy import deepcopy
import json
from tqdm import tqdm
import typo
from utils import makedir, is_good_text_column
from synthesizer.base_synthesizer import BaseSynthesizer

def generate_typo(x, error_type, random_state):
    typo_str = typo.StrErrer(x, seed=random_state)
    
    while True:
        error_type = error_type % 7
        if error_type == 0:
            typo_cell = typo_str.char_swap().result
        elif error_type == 1:
            typo_cell = typo_str.missing_char().result
        elif error_type == 2:
            typo_cell = typo_str.extra_char().result
        elif error_type == 3:
            typo_cell = typo_str.nearby_char().result
        elif error_type == 4:
            typo_cell = typo_str.similar_char().result
        elif error_type == 5:
            typo_cell = typo_str.repeated_char().result
        else:
            typo_cell = typo_str.unichar().result
        
        if typo_cell != x:
            return typo_cell
        
        error_type += 1

def inject_typo(df, random_state, error_rate=0.5):
    np.random.seed(random_state)
    if np.random.rand() < error_rate:
        num_error = np.random.randint(1, 3)
        cand_columns = [(i, c) for i, c in enumerate(df.columns) if is_good_text_column(df[c].values)]
  
        error_set = set()
        df_err = deepcopy(df)
        col_names = []
        row_indices = []
        col_indices = []
        correct_cells = []
        typo_cells =  []
        while len(error_set) < num_error:
            idx = np.random.choice(len(cand_columns))
            col_idx, col_name = cand_columns[idx]            
            row_idx = np.random.choice(len(df))
            if (row_idx, col_idx) in error_set:
                continue
            error_set.add((row_idx, col_idx))
            error_type = np.random.choice(9)
            df_values = df_err.values
            correct_cell = deepcopy(df_values[row_idx, col_idx])
            typo_cell = generate_typo(str(correct_cell), error_type, random_state)
            df_values[row_idx, col_idx] = typo_cell
            df_err = pd.DataFrame(df_values, columns=df.columns)
            
            col_names.append(col_name)
            row_indices.append(row_idx)
            col_indices.append(col_idx)
            correct_cells.append(str(correct_cell))
            typo_cells.append(str(typo_cell))
        
        return df_err, col_names, row_indices, col_indices, correct_cells, typo_cells
    else:
        return df, None, None, None, None, None

class ErrorDetectionSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "ErrorDetection"
        
    def synthesize_one(self, df_full, random_state, save_dir):
        if self.mode == "train":
            error_rate = 0.5
        else:
            error_rate = 0.2
        
        df = df_full.iloc[:5]
        
        cand_columns = [(i, c) for i, c in enumerate(df.columns) if is_good_text_column(df_full[c].values)]
        if len(cand_columns) == 0:
            return
        
        df_mv, col_name, row_idx, col_idx, correct_cell, typo_cell = inject_typo(df, random_state, error_rate=error_rate)
        
        info = {
            "error_column_name": col_name,
            "error_row_idx": row_idx,
            "error_col_idx": col_idx,
            "correct_cell": correct_cell,
            "label": typo_cell,
        }
        df_full.to_csv(makedir([save_dir], "gt.csv"), index=False)
        df_mv.to_csv(makedir([save_dir], "data.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)

        # few shot samples
        df_fewshot = df_full.iloc[5:]
        for j in range(10):
            np.random.seed(random_state+j+1)
            num_rows = np.random.randint(3, 6)
            num_rows = min(num_rows, len(df_fewshot))
            df_sample = df_fewshot.sample(n=num_rows, random_state=random_state+j+1)
            df_mv, col_name, row_idx, col_idx, correct_cell, typo_cell = inject_typo(df_sample, random_state+j+1)
            info = {
                "error_column_name": col_name,
                "error_row_idx": row_idx,
                "error_col_idx": col_idx,
                "correct_cell": correct_cell,
                "label": typo_cell,
            }
            df_sample.to_csv(makedir([save_dir, "random_fewshot_samples", f"sample_{j}"],  "gt.csv"), index=False)
            df_mv.to_csv(makedir([save_dir, "random_fewshot_samples", f"sample_{j}"], "data.csv"), index=False)
            with open(makedir([save_dir, "random_fewshot_samples", f"sample_{j}"], "info.json"), "w") as f:
                json.dump(info, f, indent=4)