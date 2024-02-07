import pandas as pd
import os
import json
from tqdm import tqdm
from utils import makedir
from synthesizer.base_synthesizer import BaseSynthesizer

class ListExtractionSynthesizer(BaseSynthesizer):
    def __init__(self):
        self.name = "ListExtraction"
        
    def synthesize_one(self, df, random_state, save_dir): 
        info = {}
        data = df.sample(n=min(len(df), 5), random_state=random_state)
        data.to_csv(makedir([save_dir], "gt.csv"), index=False)
        with open(makedir([save_dir], "info.json"), "w") as f:
            json.dump(info, f, indent=4)