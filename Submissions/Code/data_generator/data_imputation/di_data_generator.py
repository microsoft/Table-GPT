from ..base.base_data_generator import BaseDataGenerator
import os
import pandas as pd
import numpy as np
from .di_prompt_generator import DIPromptGenerator
import json
from copy import deepcopy
from .di_task_descriptor import DITaskDescriptor

class DIDataGenerator(BaseDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = DIPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = DITaskDescriptor(**params)
        return task_descriptor
    
    def _get_fewshot_datasets_info(self, test_data_info, sample_method):
        if sample_method == "random":
            # sample fewshot from entire training datasets
            fewshot_dir = os.path.join(test_data_info["dataset_dir"], "random_fewshot_samples")
        elif sample_method == "stanford":
            fewshot_dir = os.path.join(test_data_info["dataset_dir"], "stanford_fewshot_samples")
        else:
            return None
        
        if not os.path.exists(fewshot_dir):
            return None
        
        datasets_info = []
        for sample in sorted(os.listdir(fewshot_dir)):
            info = {
                "dataset_dir": os.path.join(fewshot_dir, sample)
            }
            datasets_info.append(info)
            
        fewshot_datasets_info = {
            "datasets_info": datasets_info,
            "sample_method": sample_method
        }
        return fewshot_datasets_info

    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        data_dict_perturb["data"] = data_dict_perturb["data"].sample(frac=1, axis=1, random_state=random_state)
        return data_dict_perturb

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        fewshot_data_dict_perturb = deepcopy(fewshot_data_dict)
        if fewshot_data_dict_perturb["data_label_list"] is not None:
            data_label_perturb = []
            for data, y in fewshot_data_dict_perturb["data_label_list"]:
                data_perturb = data.sample(frac=1, axis=1, random_state=random_state)
                data_label_perturb.append((data_perturb, y))
            fewshot_data_dict_perturb["data_label_list"] = data_label_perturb
        return fewshot_data_dict_perturb

    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        data = self.load_df(os.path.join(data_dir, "data.csv"))  
        y = {
            "label": info["label"],
            "cot": None
        }
        
        if self.use_cot:
            cot_data_path = self.get_cot_data_path(data_info["dataset_dir"])
            if os.path.exists(cot_data_path):
                cot_data = pd.read_csv(cot_data_path)
                y["cot"] = cot_data["cot"].values[0]

        return data, y

    
    