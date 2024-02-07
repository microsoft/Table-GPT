from ..data_imputation.di_data_generator import DIDataGenerator
import os
import pandas as pd
import numpy as np
from .rcs_prompt_generator import RCSPromptGenerator
import json
from copy import deepcopy
from .rcs_task_descriptor import RCSTaskDescriptor

class RCSDataGenerator(DIDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = RCSPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = RCSTaskDescriptor(**params)
        return task_descriptor

    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        data = self.load_df(os.path.join(data_dir, "data.csv"))
        label = self.load_df(os.path.join(data_dir, "label.csv"))        
        y = {
            "label": label,
            "cot": None
        }
        if self.use_cot:
            cot_data_path = self.get_cot_data_path(data_info["dataset_dir"])
            if os.path.exists(cot_data_path):
                cot_data = pd.read_csv(cot_data_path)
                y["cot"] = cot_data["cot"].values[0]
        return data, y
    
    def _load_task_descriptor_params(self, dataset_info):
        data_dir = dataset_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        return info
    
    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        raise

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        raise
    