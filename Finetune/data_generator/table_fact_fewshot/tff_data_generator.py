import os
import pandas as pd
import numpy as np
from ..table_fact.tf_data_generator import TFDataGenerator
from .tff_prompt_generator import TFFPromptGenerator
from .tff_task_descriptor import TFFTaskDescriptor
import json

class TFFDataGenerator(TFDataGenerator):       
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.num_few_shot_samples = 0
        self.num_few_shot_trials = 0

    def _get_prompt_generator(self, params):
        prompt_generator = TFFPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = TFFTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        return (df, info["statement"], info["caption"]), info["label"]