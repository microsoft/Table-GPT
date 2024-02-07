import pandas as pd
import numpy as np
import json
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer


class RowColumnFilteringSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "RowColumnFiltering"
        
    def manipulate(self, mode, df, column, value, column_indices, row_indices, save_dir):
        if mode == "row_filter":
            info = {
                "column": column,
                "value": value
            }
            label = df[df[column] == value]
        elif mode == "row_projection":
            row_indices = sorted(row_indices)
            info = {
                "row_indices": row_indices,
            }
            label = df.iloc[row_indices]
        else:
            columns = [df.columns[i] for i in sorted(column_indices)]
            info = {
                "columns": columns,
            }
            label = df[columns]
            
        info["type"] = mode
        df.to_csv(makedir([save_dir], "data.csv"), index=False)
        label.to_csv(makedir([save_dir], "label.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)

        
    def synthesize_one(self, df_full, random_state, save_dir):
        np.random.seed(random_state)
        df = df_full.iloc[:5].astype(str)
        mode = np.random.choice(["row_projection", "column_projection", "row_filter"])
        column = np.random.choice(df.columns)
        value = np.random.choice(sorted(set(df[column].values)))
        num_row = np.random.randint(1, len(df)-1)
        row_indices = np.random.choice(len(df), num_row, replace=False).tolist()
        num_columns = np.random.randint(1, len(df.columns)-1)
        column_indices = np.random.choice(len(df.columns), num_columns, replace=False).tolist()
        self.manipulate(mode, df, column, value, column_indices, row_indices, save_dir)
    
        df_fewshot = df_full.iloc[5:].astype(str)
        for j in range(10):
            df_sample = df_fewshot.sample(n=5, random_state=random_state+j+1).reset_index(drop=True)
            fewshot_save_dir = makedir([save_dir, "random_fewshot_samples", f"sample_{j}"])
            
            if mode == "row_filter":
                np.random.seed(random_state)
                num_sel = np.random.randint(len(df_sample)-1)
                idx = np.random.choice(len(df_sample), num_sel, replace=False)
                df_sample.loc[idx, column] = value
            
            self.manipulate(mode, df_sample, column, value, column_indices, row_indices, fewshot_save_dir)