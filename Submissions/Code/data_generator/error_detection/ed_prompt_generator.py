import pandas as pd
import numpy as np
from ..base.base_prompt_generator import BasePromptGenerator

class EDPromptGenerator(BasePromptGenerator):        
    def _shorten_input_data(self, test_data, train_samples):
        # reduce samples in fewshot examples
        if train_samples is None or len(train_samples) <= self.min_fewshot_samples:
            return test_data, train_samples, True
    
        pos_train_samples = [(data, y) for data, y in train_samples if y is not None]
        neg_train_samples = [(data, y) for data, y in train_samples if y is None]   
         
        if len(pos_train_samples) <= len(neg_train_samples):
            new_train_samples = pos_train_samples + neg_train_samples[1:]
        else:
            new_train_samples = pos_train_samples[1:] + neg_train_samples
            
        return test_data, new_train_samples, False