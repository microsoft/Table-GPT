from ..base.base_task_descriptor import BaseTaskDescriptor

class SDTaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        descriptions = [
            (
                'Given a table, values in the same column should be represented in a consistent form in order for the table to be considered "clean", because otherwise it is difficult to perform analysis and get consistent results.'
                'For example, if we have  "USA" and "United States" as two cells in the same column, that is undesirable, and we would want to standardize the two cells into a consistent representation (e.g., "USA").'
                'Given the table below, can you find cell values in the same column, that semantically correspond to the same entity, but are not represented consistently?'
                'If you find such a pair, please return both values in a list. If you did not find any inconsistent values in the same column, please return None.'
            )
        ]
        return self.select_one_option(descriptions, random_state=random_state)
    
    def get_input(self, df, random_state=None):
        return self.serializer.serialize_df(df)
    
    def _get_output(self, y):
        label = y["label"]
        if label is None:
            return "None"
        else:
            return label
        
    def get_output_example(self):
        return "inconsistent_pair", "<a list of two values from the input column>"
    
    
    