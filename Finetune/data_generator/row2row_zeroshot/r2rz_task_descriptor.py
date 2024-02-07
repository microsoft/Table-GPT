from data_generator.row2row_fewshot.r2rf_task_descriptor import R2RFTaskDescriptor
import pandas as pd
import numpy as np

class R2RZTaskDescriptor(R2RFTaskDescriptor):
        
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Transform the given input value into its corresponding output value (denoted by [Output Value]). Please only return the output value.",
        ]
        desc = self.select_one_option(descriptions, random_state=random_state)
        if self.instruction is not None:
            desc += f" (Hint: {self.instruction})"
        return desc
    
    def get_input(self, df, random_state=None):
        if random_state is not None:
            np.random.seed(random_state)
            
        df_ex = df.copy()
        df_ex = df_ex.iloc[-1:]
        df_ex.iloc[-1]["Output"] = "[Output Value]"
        prompt = self.serializer.serialize_df(df_ex)
        return prompt