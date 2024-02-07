import os
import pandas as pd
import numpy as np
from data_generator.row2row_fewshot.r2rf_data_generator import R2RFDataGenerator
from .r2rz_prompt_generator import R2RZPromptGenerator
from .r2rz_task_descriptor import R2RZTaskDescriptor
import json
from functools import partial

class R2RZDataGenerator(R2RFDataGenerator):     
    def _get_prompt_generator(self, params):
        prompt_generator = R2RZPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = R2RZTaskDescriptor(**params)
        return task_descriptor