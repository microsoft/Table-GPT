import sys
sys.path.append("../Finetune")

from data_generator.entity_matching.em_data_generator import EMDataGenerator
from .em_cot_task_descriptor import EMCOTTaskDescriptor
import json
import os

class EMCOTQueryGenerator(EMDataGenerator):             
    def _get_task_descriptor(self, params):
        task_descriptor = EMCOTTaskDescriptor(**params)
        return task_descriptor
    
    def _load_prompt_generator_params(self, dataset_info):
        info = super()._load_prompt_generator_params(dataset_info)
        info["prompt_ending"] = ""
        info["completion_ending"] = ""
        return info