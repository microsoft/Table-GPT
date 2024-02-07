from ..row_column_sorting.rcs_data_generator import RCSDataGenerator
import os
import pandas as pd
import numpy as np
from .rcsw_prompt_generator import RCSWPromptGenerator
import json
from copy import deepcopy
from .rcsw_task_descriptor import RCSWTaskDescriptor

class RCSWDataGenerator(RCSDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = RCSWPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = RCSWTaskDescriptor(**params)
        return task_descriptor
    