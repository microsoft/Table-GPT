from ..data_imputation.di_data_generator import DIDataGenerator
from .ed_prompt_generator import EDPromptGenerator
from .ed_task_descriptor import EDTaskDescriptor
import os
import json
import numpy as np
import time

class EDDataGenerator(DIDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = EDPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = EDTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        data = self.load_df(os.path.join(data_dir, "data.csv"))
        label = info["label"]
        y = {
            "label": label,
            "cot": None,
            "cot_position": self.cot_position,
            "use_cot": self.use_cot
        }
        if self.use_cot and ("correct_cell" in info) and (info["correct_cell"] is not None) and (len(info["correct_cell"]) > 0):
            cot_data = []
            for err, cor in zip(info["label"], info["correct_cell"]):
                cot_data.append((err, cor))  
            y["cot"] = cot_data      
            
        return data, y
    
    def _load_fewshot_data_dict(self, fewshot_datasets_info, num_samples, random_state):
        if num_samples == 0:
            fewshot_data_labels = None
        else:
            # balance sample and load data dict
            pos_samples = []
            neg_samples = []
        
            for sample_datasets_info in fewshot_datasets_info["datasets_info"]:
                data, y = self._load_data_label(sample_datasets_info)
                if y["label"] is None:
                    neg_samples.append((data, y))
                else:
                    pos_samples.append((data, y))

            num_neg = num_samples // 2
            num_pos = num_samples - num_neg
            pos_fewshot = self._random_sample(pos_samples, num_pos, random_state=random_state)
            neg_fewshot = self._random_sample(neg_samples, num_neg, random_state=random_state)
            fewshot_data_labels = pos_fewshot + neg_fewshot
                
        fewshot_data_dict = {
            "data_label_list": fewshot_data_labels,
            "sample_method": fewshot_datasets_info["sample_method"],
            "num_samples": num_samples,
            "random_state": random_state
        }
        return fewshot_data_dict
    