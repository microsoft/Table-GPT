import pandas as pd
import numpy as np
import json
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer


class ColumnFindingSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "ColumnFinding"
        
    def select_column(self, df):
        shuffle_column_idx = np.random.permutation(df.shape[1])
        df_values = df.values
        
        value_sel = None
        column_sel = None
        for j in shuffle_column_idx:
            if column_sel is not None:
                break
            shuffle_row_idx = np.random.permutation(len(df))
            for i in shuffle_row_idx:
                value = df_values[i, j]
                mask = (df_values == value).any(axis=1)
                if sum(mask) == 1:
                    value_sel = value
                    column_sel = df.columns[j]
                    break
        return column_sel, value_sel
        
    def synthesize_one(self, df_full, random_state, save_dir):
        if df_full.shape[1] < 8:
            return
        
        np.random.seed(random_state)
        df = df_full.iloc[:10].astype(str)
        df = df.reset_index(drop=True)
        column_sel, value_sel = self.select_column(df)
        
        if column_sel is None:
            return
        
        info = {
            "value": value_sel,
            "label": column_sel
        }
        
        df = df.to_csv(makedir([save_dir], "data.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)
        