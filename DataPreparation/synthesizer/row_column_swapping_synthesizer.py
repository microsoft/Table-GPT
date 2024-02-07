import pandas as pd
import numpy as np
import json
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer


class RowColumnSwappingSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "RowColumnSwapping"
    
    def row_swap(self, df, row_1, row_2):
        new_indices = list(range(len(df)))
        new_indices[row_1] = row_2
        new_indices[row_2] = row_1
        info = {
            "swap_row_indices": [row_1, row_2],
        }
        label = df.iloc[new_indices]
        return info, label

    def col_swap(self, df, col_1, col_2):
        new_indices = list(range(df.shape[1]))
        new_indices[col_1] = col_2
        new_indices[col_2] = col_1
        info = {
            "swap_column": [df.columns[col_1], df.columns[col_2]],
        }
        label = df.iloc[:, new_indices]
        return info, label
    
    def row_move(self, df, row_1, pos):
        new_indices = list(range(len(df)))
        if pos == "start":
            new_indices.remove(row_1)
            new_indices = [row_1] + new_indices
        else:
            new_indices.remove(row_1)
            new_indices = new_indices + [row_1]
            
        info = {
            "row_index": row_1,
            "position": pos,
        }
        label = df.iloc[new_indices]
        return info, label
    
    def col_move(self, df, col_1, pos):
        new_indices = list(range(df.shape[1]))
        if pos == "start":
            new_indices.remove(col_1)
            new_indices = [col_1] + new_indices
        else:
            new_indices.remove(col_1)
            new_indices = new_indices + [col_1]
            
        info = {
            "column": df.columns[col_1],
            "position": pos,
        }    
        label = df.iloc[:, new_indices]
        return info, label
    
    def manipulate(self, df, mode, row_1, row_2, col_1, col_2, pos, save_dir):
        if mode == "row_swapping":
            info, label = self.row_swap(df, row_1, row_2)
        elif mode == "column_swapping":
            info, label = self.col_swap(df, col_1, col_2)
        elif mode == "row_moving":
            info, label = self.row_move(df, row_1, pos)
        else:
            info, label = self.col_move(df, col_1, pos)
        info["type"] = mode
        df.to_csv(makedir([save_dir], "data.csv"), index=False)
        label.to_csv(makedir([save_dir], "label.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)

    def synthesize_one(self, df_full, random_state, save_dir):
        np.random.seed(random_state)
        df = df_full.iloc[:5].astype(str)
        df = df.reset_index(drop=True)
        mode = np.random.choice(["row_swapping", "column_swapping", "row_moving", "column_moving"])
        row_1, row_2 = np.random.choice(len(df), 2, replace=False).tolist()
        col_1, col_2 = np.random.choice(df.shape[1], 2, replace=False).tolist()
        pos = np.random.choice(["start", "end"])
        self.manipulate(df, mode, row_1, row_2, col_1, col_2, pos, save_dir)
        
        df_fewshot = df_full.iloc[5:].astype(str)
        for j in range(10):
            df_sample = df_fewshot.sample(n=5, random_state=random_state+j+1)
            fewshot_save_dir = makedir([save_dir, "random_fewshot_samples", f"sample_{j}"])
            self.manipulate(df_sample, mode, row_1, row_2, col_1, col_2, pos, fewshot_save_dir)
        
