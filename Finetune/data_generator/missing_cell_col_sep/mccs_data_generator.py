from ..base.base_data_generator import BaseDataGenerator
import os
import pandas as pd
import numpy as np
from data_generator.data_imputation.di_data_generator import DIDataGenerator
import json
from copy import deepcopy
from .mccs_task_descriptor import MCCSTaskDescriptor
from .mccs_prompt_generator import MCCSPromptGenerator

class MCCSDataGenerator(DIDataGenerator):    
    def _load_datasets(self, data_dir) -> list:
        """return a list of dictionary"""
        train_data_dir = os.path.join(data_dir, "MissingCell", "train")
        test_data_dir = os.path.join(data_dir, "MissingCell", "test")
        raw_train_datasets = self._get_datasets_info(train_data_dir)
        raw_test_datasets = self._get_datasets_info(test_data_dir)
        return raw_train_datasets, raw_test_datasets
    
    def _get_prompt_generator(self, params):
        prompt_generator = MCCSPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = MCCSTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        
        label = None
        for i in range(df.shape[1]):
            if "[MISSING]" in df.iloc[:, i].values:
                label = df.columns[i]
                break
        assert (label is not None)
        y = {
            "label": label
        }
        return df, y
    
    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        raise

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        raise
    

    