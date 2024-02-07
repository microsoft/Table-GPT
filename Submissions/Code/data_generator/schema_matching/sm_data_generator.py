import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .sm_prompt_generator import SMPromptGenerator
from .sm_task_descriptor import SMTaskDescriptor
import json
from copy import deepcopy

class SMDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = SMPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = SMTaskDescriptor(**params)
        return task_descriptor
    
    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        table1 = self.load_df(os.path.join(data_dir, "table1.csv"))
        table2 = self.load_df(os.path.join(data_dir, "table2.csv"))
        column_map = {}
        for c1, c2 in zip(info["old_headers"], info["alternative_headers"]):
            column_map[c1] = c2
        label = []
        
        for c in table1.columns:
            if c not in column_map:
                label.append((c, None))
            else:
                c2 = column_map[c]
                if c2 in table2.columns:
                    label.append((c, c2))
                else:
                    label.append((c, None))
                
        return (table1, table2), label
    
    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        np.random.seed(random_state)
        t1, t2 = data_dict_perturb["data"]
        t1 = t1.sample(frac=1, axis=1)
        t2 = t2.sample(frac=1, axis=1)
        data_dict_perturb["data"] = (t1, t2)
        label_dict = {c1: c2 for c1, c2 in data_dict_perturb["label"]}
        data_dict_perturb["label"] = [(c, label_dict[c]) for c in t1.columns]
        return data_dict_perturb

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        fewshot_data_dict_perturb = deepcopy(fewshot_data_dict)
        np.random.seed(random_state)
        if fewshot_data_dict_perturb["data_label_list"] is not None:
            data_label_perturb = []
            for (t1, t2), y in fewshot_data_dict_perturb["data_label_list"]:
                t1 = t1.sample(frac=1, axis=1)
                t2 = t2.sample(frac=1, axis=1)
                data_perturb = (t1, t2)
                label_dict = {c1: c2 for c1, c2 in y}
                y_perturb = [(c, label_dict[c]) for c in t1.columns]
                data_label_perturb.append((data_perturb, y_perturb))
                
            fewshot_data_dict_perturb["data_label_list"] = data_label_perturb
        return fewshot_data_dict_perturb