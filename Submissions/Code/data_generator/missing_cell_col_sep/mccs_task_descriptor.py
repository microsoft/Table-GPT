from ..base.base_task_descriptor import BaseTaskDescriptor

class MCCSTaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, missing_token="[MISSING]", **kwargs):
        super().__init__(**kwargs)
        self.missing_token = missing_token
        
    def _get_task_description(self, random_state=None):
        descriptions = [
           'Please check the following table, there is one and exactly one cell in the table that is missing. When you find this missing cell, please point it out using its column name.'
        ]
        return self.select_one_option(descriptions, random_state=random_state)
        
    def get_input(self, df, random_state=None):
        input_text = self.serializer.serialize_df(df)
        return input_text.replace("[MISSING]", "")
    
    def _get_output(self, y):
        label = str(y["label"])
        return label
    
    def get_output_example(self):
        return "missing_col", "<missing column name>"