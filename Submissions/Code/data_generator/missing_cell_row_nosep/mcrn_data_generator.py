from ..base.base_data_generator import BaseDataGenerator
import os
import pandas as pd
import numpy as np
from data_generator.missing_cell_row_sep.mcrs_data_generator import MCRSDataGenerator
import json
from copy import deepcopy

from .mcrn_task_descriptor import MCRNTaskDescriptor
from .mcrn_prompt_generator import MCRNPromptGenerator

class MCRNDataGenerator(MCRSDataGenerator):    
    def _get_prompt_generator(self, params):
        prompt_generator = MCRNPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = MCRNTaskDescriptor(**params)
        return task_descriptor
    