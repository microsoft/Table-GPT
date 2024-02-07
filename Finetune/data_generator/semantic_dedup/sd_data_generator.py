from .sd_prompt_generator import SDPromptGenerator
from ..error_detection.ed_data_generator import EDDataGenerator
from .sd_task_descriptor import SDTaskDescriptor
import os
import json
import numpy as np
import time

class SDDataGenerator(EDDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = SDPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = SDTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        data = self.load_df(os.path.join(data_dir, "data.csv"))
        label = info["label"]
        y = {
            "label": label,
        }
        return data, y