from ..base.base_prompt_generator import BasePromptGenerator
import pandas as pd

class EMPromptGenerator(BasePromptGenerator):
    def __init__(self, unimportant_columns=[], **kwargs):
        super().__init__(**kwargs)
        self.unimportant_columns = unimportant_columns
        
    def _shorten_input_data(self, test_data, train_samples):
        # make train samples less
        if train_samples is not None and len(train_samples) > self.min_fewshot_samples:
            pos_train_samples = [(data, y) for data, y in train_samples if y["label"] == '1']
            neg_train_samples = [(data, y) for data, y in train_samples if y["label"] == '0']
            
            if len(pos_train_samples) < len(neg_train_samples):
                new_train_samples = pos_train_samples + neg_train_samples[1:]
            else:
                new_train_samples = pos_train_samples[1:] + neg_train_samples
            
            return test_data, new_train_samples, False
        
        # try drop very long and na column
        row_l, row_r = test_data
        
        # only drop na columns and very long column or unimportant columns
        row_l_nona = self.drop_long_na_column(row_l)
        row_r_nona = self.drop_long_na_column(row_r)

        if train_samples is not None:
            train_samples_nona = []
            for (l, r), y in train_samples:
                l_nona = self.drop_long_na_column(l)
                r_nona = self.drop_long_na_column(r)
                data_nona = (l_nona, r_nona)
                train_samples_nona.append((data_nona, y))
        else:
            train_samples_nona = None
        
        return (row_l_nona, row_r_nona), train_samples_nona, False

    def drop_long_na_column(self, row):
        new_index = []
        for x in row.index:
            if len(str(row[x])) <= 150 and not pd.isna(row[x]) and str(row[x]).lower() != "nan" and x not in self.unimportant_columns:
                new_index.append(x)
        return row[new_index]