import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .ns_prompt_generator import NSPromptGenerator
import json
from .ns_task_descriptor import NSTaskDescriptor

class NSDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = NSPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = NSTaskDescriptor(**params)
        return task_descriptor

    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        data = (df, info["question"])
        label = info["label"]
        return data, label