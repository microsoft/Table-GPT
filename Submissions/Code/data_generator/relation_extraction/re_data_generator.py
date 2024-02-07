from ..base.base_data_generator import BaseDataGenerator
import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
import json
from copy import deepcopy
from .re_task_descriptor import RETaskDescriptor
from .re_prompt_generator import REPromptGenerator

class REDataGenerator(BaseDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = REPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = RETaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        label = info["label"]
        candidates = info["candidates"]
        return (df, candidates), label
    
    def _load_task_descriptor_params(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        params = {
            "page_title": info["page_title"],
            "table_title": info["table_title"]
        }
        return params