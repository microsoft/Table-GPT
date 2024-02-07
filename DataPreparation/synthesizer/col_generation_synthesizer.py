import pandas as pd
import os
import numpy as np
from copy import deepcopy
import json
from tqdm import tqdm
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer

class ColGenerationSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "ColGeneration"
        
    def synthesize_one(self, df_full, random_state, save_dir):
        df = df_full.iloc[:10, :10]
        
        df_test = df.iloc[:, :-1]
        df_label = [df.columns[-1]] + [str(x) for x in df.iloc[:, -1].values]
        info = {
            "label": df_label
        }
        df_test.to_csv(makedir([save_dir], "data.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)