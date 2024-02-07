import numpy as np
from ..base.base_data_generator import BaseDataGenerator
from .hvm_prompt_generator import HVMPromptGenerator
from .hvm_task_descriptor import HVMTaskDescriptor
from copy import deepcopy

class HVMDataGenerator(BaseDataGenerator):                    
    def _get_prompt_generator(self, params):
        params["max_token_length"] -= 100
        prompt_generator = HVMPromptGenerator(**params)
        return prompt_generator
    
    def _get_task_descriptor(self, params):
        task_descriptor = HVMTaskDescriptor(**params)
        return task_descriptor

    def col_perturb_helper(self, df, label):
        new_order = np.random.permutation(df.shape[1])
        old_columns = list(df.columns)
        new_columns = [old_columns[i] for i in new_order]
        df_perturb = df[new_columns]
        label_perturb = [label[i] for i in new_order]
        return df_perturb, label_perturb
    
    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        np.random.seed(random_state)
        df = data_dict_perturb["data"]
        label = data_dict_perturb["label"]
        df_perturb, label_perturb = self.col_perturb_helper(df, label)
        data_dict_perturb["data"] = df_perturb
        data_dict_perturb["label"] = label_perturb
        return data_dict_perturb

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        np.random.seed(random_state)
        fewshot_data_dict_perturb = deepcopy(fewshot_data_dict)
        if fewshot_data_dict_perturb["data_label_list"] is not None:
            data_label_perturb = []
            for data, y in fewshot_data_dict_perturb["data_label_list"]:
                data_perturb, label_perturb = self.col_perturb_helper(data, y)
                data_label_perturb.append((data_perturb, label_perturb))
            fewshot_data_dict_perturb["data_label_list"] = data_label_perturb
        return fewshot_data_dict_perturb