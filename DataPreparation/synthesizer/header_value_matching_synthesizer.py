import pandas as pd
import sys
import os
import numpy as np
import json
from tqdm import tqdm
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer

class HeaderValueMatchingSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "HeaderValueMatching"

    def synthesize_one(self, df, random_state, save_dir):
        np.random.seed(random_state)
        header = [str(c) for c in df.columns]
        header_shuffled = np.random.permutation(header)
        data = pd.DataFrame(df.values, columns=header_shuffled)
        info = {
            "label": header,
        }
        data = data.sample(n=min(len(data), 5), random_state=random_state)
        data.to_csv(makedir([save_dir], "data.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)