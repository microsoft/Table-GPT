import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .glue_prompt_generator import GluePromptGenerator
from .glue_task_descriptor import GlueTaskDescriptor
import json

class GlueDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = GluePromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = GlueTaskDescriptor(**params)
        return task_descriptor
    
    def _load_task_descriptor_params(self, dataset_info):
        return {"task": self.task}
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        return info, info
    
    def _load_fewshot_data_dict(self, fewshot_datasets_info, num_samples, random_state):
        if fewshot_datasets_info is None:
            return None
        
        if num_samples == 0:
            fewshot_data_labels = None
    
        elif "mnli" in self.task:
            return super()._load_fewshot_data_dict(fewshot_datasets_info, num_samples, random_state)
        else:
            # take a sample and load data dict
            # sample_datasets_info = self._random_sample(fewshot_datasets_info["datasets_info"], num_samples, random_state)
            pos_samples = []
            neg_samples = []
        
            for sample_datasets_info in fewshot_datasets_info["datasets_info"]:
                data, y = self._load_data_label(sample_datasets_info)
                if y["label"] == 0:
                    neg_samples.append((data, y))
                elif y["label"] == 1:
                    pos_samples.append((data, y))
                else:
                    raise Exception(f"Wrong label to use balance sample {y['label']}")

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
    