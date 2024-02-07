import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .cta_prompt_generator import CTAPromptGenerator
from .cta_task_descriptor import CTATaskDescriptor
import json

class CTADataGenerator(BaseDataGenerator):   
    def _get_prompt_generator(self, params):
        prompt_generator = CTAPromptGenerator(**params)
        return prompt_generator

    def _get_task_descriptor(self, params):
        task_descriptor = CTATaskDescriptor(**params)
        return task_descriptor
    
    def _get_datasets_info(self, data_dir):
        datasets = []
        if not os.path.exists(data_dir):
            print("Not Exists Warning:", data_dir)
            return datasets
        for benchmark in sorted(os.listdir(data_dir)):
            for dataset in sorted(os.listdir(os.path.join(data_dir, benchmark))):
                with open(os.path.join(data_dir, benchmark, dataset, "info.json"), "r") as f:
                    info = json.load(f)
                dataset_info = {
                    "benchmark": benchmark,
                    "dataset": dataset,
                    "dataset_dir": os.path.join(data_dir, benchmark, dataset),
                    "label": info["label"]
                }
                datasets.append(dataset_info)
        return datasets
    
    def _load_fewshot_data_dict(self, fewshot_datasets_info, num_samples, random_state):
        if num_samples == 0:
            fewshot_data_labels = None
        else:
            # balance sample
            pos_samples = []
            neg_samples = []
            
            np.random.seed(random_state)
            pos_train_datasets = []
            neg_train_datasets = []
            
            for dataset_info in fewshot_datasets_info["datasets_info"]:
                if dataset_info["label"] is None:
                    neg_train_datasets.append(dataset_info)
                else:
                    pos_train_datasets.append(dataset_info)
            
            neg_num = min(num_samples // 2, len(neg_train_datasets))
            pos_num = num_samples - neg_num
            
            if neg_num > 0:
                neg_samples_indices = np.random.choice(len(neg_train_datasets), neg_num, replace=False).tolist()
                neg_samples = [neg_train_datasets[i] for i in neg_samples_indices]
            if pos_num > 0:
                pos_samples_indices = np.random.choice(len(pos_train_datasets), pos_num, replace=False).tolist()
                pos_samples = [pos_train_datasets[i] for i in pos_samples_indices]
                
            sample_datasets_info = pos_samples + neg_samples
            
            fewshot_data_labels = []
            for dataset_info in sample_datasets_info:
                data, label = self._load_data_label(dataset_info)
                fewshot_data_labels.append((data, label))
                
        fewshot_data_dict = {
            "data_label_list": fewshot_data_labels,
            "sample_method": fewshot_datasets_info["sample_method"],
            "num_samples": num_samples,
            "random_state": random_state
        }
        return fewshot_data_dict

    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        df = self.load_df(os.path.join(data_dir, "data.csv"))
        label = info["label"]
        candidates = info["candidates"]
        return (df, candidates), label
    
    def _load_metadata(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        candidates = info["candidates"]
        if candidates is None:
            num_cand = 0
        else:
            num_cand = len(candidates)
        
        metadata = {
            "numCandidates": num_cand
        }
        return metadata

    def _get_fewshot_datasets_info(self, test_data_info, sample_method):
        if sample_method == "random":
            datasets_info = []
            for data_info in self.raw_train_datasets:
                train_name = data_info["benchmark"]
                test_name = test_data_info["benchmark"]
                
                if train_name.endswith("Train"):
                    train_name = train_name[:-5]
                    
                if test_name.endswith("Test"):
                    test_name = test_name[:-4]
                elif test_name.endswith("Train"):
                    test_name = test_name[:-5]
                    
                if train_name == test_name:
                    datasets_info.append(data_info)
            
            fewshot_datasets_info = {
                "datasets_info": datasets_info,
                "sample_method": "random"
            }
            return fewshot_datasets_info
        else:
            return None