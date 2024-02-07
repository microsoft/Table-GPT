from ..base.base_data_generator import BaseDataGenerator
import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
import json
from copy import deepcopy
from .cf_task_descriptor import CFTaskDescriptor
from .cf_prompt_generator import CFPromptGenerator

class CFDataGenerator(BaseDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = CFPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = CFTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        label = info["label"]
        value = info["value"]
        return (df, value), label
    