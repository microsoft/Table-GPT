import sys
sys.path.append("../Finetune")

from data_generator.row_column_swapping.rcsw_data_generator import RCSWDataGenerator
from .rcsw_cot_task_descriptor import RCSWCOTTaskDescriptor
import json
import os

class RCSWCOTQueryGenerator(RCSWDataGenerator):     
    def _get_task_descriptor(self, params):
        task_descriptor = RCSWCOTTaskDescriptor(**params)
        return task_descriptor
    
    def _load_prompt_generator_params(self, dataset_info):
        info = super()._load_prompt_generator_params(dataset_info)
        info["prompt_ending"] = ""
        info["completion_ending"] = ""
        return info

    def _get_datasets_info(self, data_dir):
        datasets = []
        if not os.path.exists(data_dir):
            print("Not Exists Warning:", data_dir)
            return datasets
        for benchmark in sorted(os.listdir(data_dir)):
            for dataset in sorted(os.listdir(os.path.join(data_dir, benchmark))):
                dataset_info = {
                    "benchmark": benchmark,
                    "dataset": dataset,
                    "dataset_dir": os.path.join(data_dir, benchmark, dataset),
                }
                datasets.append(dataset_info)
                if os.path.exists(os.path.join(data_dir, benchmark, dataset, "random_fewshot_samples")):
                    for sample in os.listdir(os.path.join(data_dir, benchmark, dataset, "random_fewshot_samples")):
                        dataset_info = {
                            "benchmark": benchmark,
                            "dataset": os.path.join(dataset, "random_fewshot_samples", sample),
                            "dataset_dir": os.path.join(data_dir, benchmark, dataset, "random_fewshot_samples", sample),
                        }
                        datasets.append(dataset_info)
        return datasets