import pandas as pd
import numpy as np
import json
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer


class RowColumnSortingSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "RowColumnSorting"
    
    def manipulate(self, df, mode, ascending, column, save_dir):
        if mode == "row":
            info = {
                "sortby": column,
                "ascending": ascending
            }
            label = df.sort_values(by=column, ascending=ascending)
        else:
            info = {
                "ascending": ascending
            }
            if ascending:
                new_columns = sorted(df.columns)
            else:
                new_columns = sorted(df.columns)[::-1]
            
            label = df[new_columns]
        info["type"] = mode
        
        df.to_csv(makedir([save_dir], "data.csv"), index=False)
        label.to_csv(makedir([save_dir], "label.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)
        
        
    def synthesize_one(self, df_full, random_state, save_dir):
        np.random.seed(random_state)
        mode = np.random.choice(["row", "column"])
        df = df_full.iloc[:5].astype(str)
        df = df.reset_index(drop=True)
        
        ascending = np.random.rand() < 0.5
        column = np.random.choice(df.columns)
        self.manipulate(df, mode, ascending, column, save_dir)

        df_fewshot = df_full.iloc[5:].astype(str)
        for j in range(10):
            df_sample = df_fewshot.sample(n=5, random_state=random_state+j+1)
            fewshot_save_dir = makedir([save_dir, "random_fewshot_samples", f"sample_{j}"])
            self.manipulate(df_sample, mode, ascending, column, fewshot_save_dir)