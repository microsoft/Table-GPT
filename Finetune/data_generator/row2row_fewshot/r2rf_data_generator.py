import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .r2rf_prompt_generator import R2RFPromptGenerator
from .r2rf_task_descriptor import R2RFTaskDescriptor
import json
from functools import partial

class R2RFDataGenerator(BaseDataGenerator):     
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs) 
        # no few shot for row transformation
        self.num_few_shot_samples = 0
        self.num_few_shot_trials = 0
        self.prob_train_few_shot = 0

    def _load_datasets(self, data_dir) -> list:
        """return a list of dictionary"""
        train_data_dir = os.path.join(data_dir, "Row2Row", "train")
        test_data_dir = os.path.join(data_dir, "Row2Row", "test")
        raw_train_datasets = self._get_datasets_info(train_data_dir)
        raw_test_datasets = self._get_datasets_info(test_data_dir)
        return raw_train_datasets, raw_test_datasets
        
    def _load_task_descriptor_params(self, dataset_info):
        with open(os.path.join(dataset_info["dataset_dir"], "info.json"), "r") as f:
            info = json.load(f)
        params = {
            "instruction": info["instruction"]
        }
        return params
            
    def _get_prompt_generator(self, params):
        prompt_generator = R2RFPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = R2RFTaskDescriptor(**params)
        return task_descriptor
    
    def _load_metadata(self, data_info):
        with open(os.path.join(data_info["dataset_dir"], "info.json"), "r") as f:
            info = json.load(f)
        metadata = {
            "filename": info["filename"]
        }
        return metadata
    
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
    
