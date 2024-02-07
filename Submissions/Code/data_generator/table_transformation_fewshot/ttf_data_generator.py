import os
import pandas as pd
import numpy as np
from data_generator.table_transformation_zeroshot.ttz_data_generator import TTZDataGenerator
import json
from copy import deepcopy
from .ttf_task_descriptor import TTFTaskDescriptor
from .ttf_prompt_generator import TTFPromptGenerator

class TTFDataGenerator(TTZDataGenerator):        
    def _get_prompt_generator(self, params):
        prompt_generator = TTFPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = TTFTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        labels = info["label"][0].split("-")
        invalid_list = [
            "multistep_notebook_T48",
            "multistep_excel_file_T29",
            "transpose_notebook_T43",
            "stack_notebook_T36",
            "transpose_notebook_T45",
            "transpose_notebook_T49",
            "multistep_excel_file_T82",
            "explode_notebook_T2",
        ]
        result = []
        for label in labels:
            op, params = self.get_op_params(label)
            
            if op not in ["pivot", "subtitle", "explode"]:
                df = df.iloc[:5]
            else:
                df = df.iloc[:15]
            
            max_col = 50
            
            df = df.iloc[:, :max_col]
            if op == "stack":
                params["stack_end_idx"] = min(params["stack_end_idx"], max_col-1)
            if op == "wide_to_long":
                params["wide_to_long_end_idx"] = min(params["wide_to_long_end_idx"], max_col-1)
            if op == "explode":
                params["explode_column_idx"] = min(params["explode_column_idx"], max_col-1)
                
            y = {
                "transformation": op
            }
            
            y.update(params)
            result.append(y)
        
        if data_info["dataset"] == "explode_notebook_T2":
            df = df.iloc[:2] 
            
        if data_info["dataset"] == "explode_excel_file_T13":
            df = df.iloc[:5]

        if data_info["dataset"] in invalid_list:
            df = df.iloc[:3]
        
        if data_info["dataset"] == "transpose_notebook_T49":
            df = df.iloc[:, :30]
            
        if len(result) == 1:
            return df, result[0]
        else:
            return df, result

    