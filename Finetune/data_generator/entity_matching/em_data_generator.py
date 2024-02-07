import numpy as np
import pandas as pd
from utils import balance_sample_two_classes, makedir
from collections import defaultdict
from copy import deepcopy
from tqdm import tqdm
from multiprocessing import Pool
from .em_prompt_generator import EMPromptGenerator
from .em_task_descriptor import EMTaskDescriptor
from ..base.base_data_generator import BaseDataGenerator
import json
import os
from functools import partial

class EMDataGenerator(BaseDataGenerator):
    def _get_prompt_generator(self, params):
        prompt_generator = EMPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = EMTaskDescriptor(**params)
        return task_descriptor
    
    def _load_prompt_generator_params(self, dataset_info):
        with open(os.path.join(dataset_info["dataset_dir"], "info.json"), "r") as f:
            info = json.load(f)
        unimportant_columns = info["unimportant_columns"] if "unimportant_columns" in info else []
        params = {
            "unimportant_columns": unimportant_columns
        }
        return params
    
    def _load_task_descriptor_params(self, dataset_info):
        with open(os.path.join(dataset_info["dataset_dir"], "info.json"), "r") as f:
            info = json.load(f)
        topic = info["topic"] if "topic" in info else "Entity"
        params = {
            "topic": topic
        }
        return params
    
    def _load_datasets(self, data_dir) -> list:
        """return a list of dictionary"""
        train_data_dir = os.path.join(data_dir, self.task, "train")
        test_data_dir = os.path.join(data_dir, self.task, "test")
        raw_train_datasets = self._get_datasets_info(train_data_dir, "train")
        raw_test_datasets = self._get_datasets_info(test_data_dir, "test")
        return raw_train_datasets, raw_test_datasets
    
    def _get_datasets_info(self, data_dir, mode):
        datasets = []
        for benchmark in sorted(os.listdir(data_dir)):
            for dataset in sorted(os.listdir(os.path.join(data_dir, benchmark))):
                gt = pd.read_csv(os.path.join(data_dir, benchmark, dataset, f"{mode}.csv"))
                for i in range(len(gt)):
                    dataset_info = {
                        "benchmark": benchmark,
                        "dataset": dataset,
                        "dataset_dir": os.path.join(data_dir, benchmark, dataset),
                        "mode": mode,
                        "row_id": i,
                    }
                    datasets.append(dataset_info)
        return datasets

    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
            
        left = self.load_df(os.path.join(data_dir, "tableA.csv"), info=info)
        right = self.load_df(os.path.join(data_dir, "tableB.csv"), info=info)
        gt = self.load_df(os.path.join(data_dir, f"{data_info['mode']}.csv"))
        
        left = left.set_index("id")
        right = right.set_index("id")
        
        row = gt.iloc[data_info["row_id"]]
        row_l = left.loc[row.ltable_id]
        row_r = right.loc[row.rtable_id]
        label = row.label
        data = (row_l, row_r)
        
        y = {
            "label": label,
            "cot": None,
            "cot_position": self.cot_position
        }
        
        if self.use_cot:
            cot_data_path = os.path.join(self.cot_data_dir, self.task, data_info['mode'], data_info["benchmark"], data_info["dataset"], "data.csv")
            if os.path.exists(cot_data_path):
                cot_data = pd.read_csv(cot_data_path)
                cot_data = cot_data.set_index("lrid")
                if f"{row.ltable_id}-{row.rtable_id}" in cot_data.index:
                    row_cot = cot_data.loc[f"{row.ltable_id}-{row.rtable_id}"]
                    y["cot"] = row_cot["cot"]
        return data, y
    
    def _load_metadata(self, data_info):
        gt = self.load_df(os.path.join(data_info["dataset_dir"], f"{data_info['mode']}.csv"))
        row = gt.iloc[data_info["row_id"]]
        metadata = {
            "lrid": f"{row.ltable_id}-{row.rtable_id}"
        }
        return metadata
    
    def _get_fewshot_datasets_info(self, test_data_info, sample_method):
        if sample_method == "random":
            data_dir = test_data_info["dataset_dir"]
            
            with open(os.path.join(data_dir, "info.json"), "r") as f:
                info = json.load(f)
                
            left = self.load_df(os.path.join(data_dir, "tableA.csv"), info=info)
            right = self.load_df(os.path.join(data_dir, "tableB.csv"), info=info)
            train = self.load_df(os.path.join(data_dir, "train.csv"))
            
            cot_data = None
            if self.use_cot:
                cot_data_path = os.path.join(self.cot_data_dir, self.task, test_data_info['mode'], test_data_info["benchmark"], test_data_info["dataset"], "data.csv")
                if os.path.exists(cot_data_path):
                    cot_data = pd.read_csv(cot_data_path)
                    cot_data = cot_data.set_index("lrid")
            
            fewshot_datasets_info = {
                "gt": train,
                "left": left.set_index("id"),
                "right": right.set_index("id"),
                "sample_method": sample_method,
                "cot_data": cot_data
            }
            return fewshot_datasets_info
        else:
            return None
        
    def _load_fewshot_data_dict(self, fewshot_datasets_info, num_samples, random_state):
        if num_samples == 0:
            fewshot_data_labels = None
        else:
            # take a sample and load data dict
            fewshot_sample_gt = balance_sample_two_classes(fewshot_datasets_info["gt"], num_samples, random_state=random_state)
            fewshot_data_labels= []
            for _, row in fewshot_sample_gt.iterrows():
                l = fewshot_datasets_info["left"].loc[row.ltable_id]
                r = fewshot_datasets_info["right"].loc[row.rtable_id]
                data = (l, r)
                label = row.label
                cot_text = None
                if self.use_cot and fewshot_datasets_info["cot_data"] is not None:
                    if f"{row.ltable_id}-{row.rtable_id}" in fewshot_datasets_info["cot_data"].index:
                        cot_text = fewshot_datasets_info["cot_data"].loc[f"{row.ltable_id}-{row.rtable_id}"]["cot"]

                y = {
                    "label": label,
                    "cot": cot_text,
                    "cot_position": self.cot_position
                }
                fewshot_data_labels.append((data, y))
                
        fewshot_data_dict = {
            "data_label_list": fewshot_data_labels,
            "sample_method": fewshot_datasets_info["sample_method"],
            "num_samples": num_samples,
            "random_state": random_state
        }
        return fewshot_data_dict
    
    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        row_l, row_r = data_dict_perturb["data"]
        row_l_perturb = row_l.sample(frac=1, random_state=random_state)
        row_r_perturb = row_r.sample(frac=1, random_state=random_state)
        data_dict_perturb["data"] = (row_l_perturb, row_r_perturb)
        return data_dict_perturb

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        fewshot_data_dict_perturb = deepcopy(fewshot_data_dict)
        if fewshot_data_dict_perturb["data_label_list"] is not None:
            data_label_perturb = []
            for data, y in fewshot_data_dict_perturb["data_label_list"]:
                row_l, row_r = data
                row_l_perturb = row_l.sample(frac=1, random_state=random_state)
                row_r_perturb = row_r.sample(frac=1, random_state=random_state)
                data_perturb = (row_l_perturb, row_r_perturb)
                data_label_perturb.append((data_perturb, y))
            fewshot_data_dict_perturb["data_label_list"] = data_label_perturb
        return fewshot_data_dict_perturb

    