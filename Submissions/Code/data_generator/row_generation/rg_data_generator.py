import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .rg_prompt_generator import RGPromptGenerator
from .rg_task_descriptor import RGTaskDescriptor
import json

class RGDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = RGPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = RGTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        data = self.load_df(os.path.join(data_dir, "data.csv"))
        new_row = pd.DataFrame([info["label"]], columns=data.columns)
        new_df = pd.concat([data, new_row], axis=0).reset_index(drop=True)
        return data, new_df