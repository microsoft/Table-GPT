import os
import pandas as pd
import numpy as np
from data_generator.base.base_data_generator import BaseDataGenerator
import json
from copy import deepcopy
from .ttz_task_descriptor import TTZTaskDescriptor
from .ttz_prompt_generator import TTZPromptGenerator
    
class TTZDataGenerator(BaseDataGenerator):   
    def _load_datasets(self, data_dir) -> list:
        """return a list of dictionary"""
        train_data_dir = os.path.join(data_dir, "TableTransformation", "train")
        test_data_dir = os.path.join(data_dir, "TableTransformation", "test")
        raw_train_datasets = self._get_datasets_info(train_data_dir)
        raw_test_datasets = self._get_datasets_info(test_data_dir)
        return raw_train_datasets, raw_test_datasets
     
    def _get_prompt_generator(self, params):
        prompt_generator = TTZPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = TTZTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        labels = info["label"][0].split("-")
        
        result = []
        for label in labels:
            op, params = self.get_op_params(label)
            
            if op not in ["pivot", "subtitle", "explode"]:
                df = df.iloc[:5]
            else:
                df = df.iloc[:15]
                    
            df = df.iloc[:, :50]
            if op == "stack":
                params["stack_end_idx"] = min(params["stack_end_idx"], 49)
            if op == "wide_to_long":
                params["wide_to_long_end_idx"] = min(params["wide_to_long_end_idx"], 49)
            if op == "explode":
                params["explode_column_idx"] = min(params["explode_column_idx"], 49)
                
            y = {
                "transformation": op
            }
            
            y.update(params)
            result.append(y)
        
        if data_info["dataset"] == "explode_notebook_T2":
            df = df.iloc[:3] 
            
        if len(result) == 1:
            return df, result[0]
        else:
            return df, result
    
    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        raise

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        raise
    
    def get_op_params(self, label):
        if "wide_to_long" in label:
            op = "wide_to_long"
        else:
            op = label.split("_")[0]
            
        if op == "wide_to_long":
            params = {
                "wide_to_long_start_idx": int(label.split("_")[-2]),
                "wide_to_long_end_idx": int(label.split("_")[-1]) - 1
            }
        elif op == "stack":
            params = {
                "stack_start_idx": int(label.split("_")[-2]),
                "stack_end_idx": int(label.split("_")[-1]) - 1
            }
        elif op == "explode":
            params = {
                "explode_column_idx": int(label.split("_")[-1])
            }
        elif op == "pivot":
            params = {
                "pivot_row_frequency": int(label.split("_")[-1])
            }    
        elif op == "ffill":
            params = {
                "ffill_end_idx": int(label.split("_")[-1]) - 1
            }
        else:
            params = {}
        return op, params
    

    