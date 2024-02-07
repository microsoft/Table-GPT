from ..base.base_task_descriptor import BaseTaskDescriptor

class CFTaskDescriptor(BaseTaskDescriptor):        
    def _get_task_description(self, random_state=None):
        descriptions = [
           f'Please look at the table below and find the column that contains the given cell value.'
        ]
        return self.select_one_option(descriptions, random_state=random_state)
        
    def get_input(self, data, random_state=None):
        df, cell_value = data

        prompt = (
            "**Input Table:**\n"
            f"{self.serializer.serialize_df(df)}\n"
            "**Given Cell Value:**\n"
            f"{cell_value}\n"
        )
        
        return prompt
    
    def get_output_example(self):
        return "result", "<name of the column containing the given cell value>"
    
    def _get_output(self, y):
        label = str(y)
        return label