import os
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .le_prompt_generator import LEPromptGenerator
from .le_task_descriptor import LETaskDescriptor
import json
from copy import deepcopy

class LEDataGenerator(BaseDataGenerator):         
    def _get_prompt_generator(self, params):
        params["max_token_length"] = params["max_token_length"] / 2 
        prompt_generator = LEPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = LETaskDescriptor(**params)
        return task_descriptor
       
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        data = self.load_df(os.path.join(data_dir, "gt.csv"))
        label = self.load_df(os.path.join(data_dir, "gt.csv"))
        return data, label
        
    def _augment_train_data_col_perturb(self, data_dict, random_state) -> dict:
        data_dict_perturb = deepcopy(data_dict)
        np.random.seed(random_state)
        data_perturb = data_dict_perturb["data"].sample(frac=1, axis=1)
        data_dict_perturb["data"] = data_perturb
        data_dict_perturb["label"] = data_perturb
        
        few_shot_samples_perturb = []
        for data, y in data_dict_perturb["few_shot_samples"]:
            data_perturb = data.sample(frac=1, axis=1)
            few_shot_samples_perturb.append((data_perturb, data_perturb))
            
        data_dict_perturb["few_shot_samples"] = few_shot_samples_perturb
        return data_dict_perturb
    
    