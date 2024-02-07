import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .tq_prompt_generator import TQPromptGenerator
from .tq_task_descriptor import TQTaskDescriptor
import json

class TQDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = TQPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = TQTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        return (df, info["question"]), info["label"]