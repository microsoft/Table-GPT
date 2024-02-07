import sys
sys.path.append("../Finetune")

from data_generator.row2row_fewshot.r2rf_data_generator import R2RFDataGenerator
from .r2rf_cot_task_descriptor import R2RFCOTTaskDescriptor
import json
import os

class R2RFCOTQueryGenerator(R2RFDataGenerator):     
    def _get_task_descriptor(self, params):
        task_descriptor = R2RFCOTTaskDescriptor(**params)
        return task_descriptor
    
    def _load_prompt_generator_params(self, dataset_info):
        info = super()._load_prompt_generator_params(dataset_info)
        info["prompt_ending"] = ""
        info["completion_ending"] = ""
        return info