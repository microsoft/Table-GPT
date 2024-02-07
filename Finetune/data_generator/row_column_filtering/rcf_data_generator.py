from ..row_column_sorting.rcs_data_generator import RCSDataGenerator
import os
import pandas as pd
import numpy as np
from .rcf_prompt_generator import RCFPromptGenerator
import json
from copy import deepcopy
from .rcf_task_descriptor import RCFTaskDescriptor

class RCFDataGenerator(RCSDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = RCFPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = RCFTaskDescriptor(**params)
        return task_descriptor
    