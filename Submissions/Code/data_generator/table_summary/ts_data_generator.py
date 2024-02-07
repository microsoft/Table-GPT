import os
import pandas as pd
import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .ts_prompt_generator import TSPromptGenerator
from .ts_task_descriptor import TSTaskDescriptor
import json

class TSDataGenerator(BaseDataGenerator):            
    def _get_prompt_generator(self, params):
        prompt_generator = TSPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = TSTaskDescriptor(**params)
        return task_descriptor