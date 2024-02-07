import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .cg_prompt_generator import CGPromptGenerator
from .cg_task_descriptor import CGTaskDescriptor
import json

class CGDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = CGPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = CGTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        data = self.load_df(os.path.join(data_dir, "data.csv"))
        new_col = pd.DataFrame({info["label"][0]: info["label"][1:]})
        new_df = pd.concat([data, new_col], axis=1)
        return data, new_df