from ..base.base_data_generator import BaseDataGenerator
import os
import pandas as pd
import numpy as np
from data_generator.missing_cell_col_sep.mccs_data_generator import MCCSDataGenerator
import json
from copy import deepcopy

from .mccn_task_descriptor import MCCNTaskDescriptor
from .mccn_prompt_generator import MCCNPromptGenerator

class MCCNDataGenerator(MCCSDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = MCCNPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = MCCNTaskDescriptor(**params)
        return task_descriptor
    