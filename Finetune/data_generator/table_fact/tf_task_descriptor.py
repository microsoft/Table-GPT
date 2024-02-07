from ..base.base_task_descriptor import BaseTaskDescriptor

class TFTaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Please look at the table, and then determine whether the statement is True or False based on the table. Ensure that your response is only based on the information within the input table and does not involve any external information."
        ]
        return self.select_one_option(descriptions, random_state=random_state)

    def get_input(self, data, random_state=None):
        df, statement, caption = data
        text = (
            f"*Table Caption:* {caption}\n"
            "*Table:*\n"
            f"{self.serializer.serialize_df(df)}\n"
            "*Statement:*\n"
            f"{statement}"
        )
        return text
    
    def _get_output(self, y):
        if y == 0:
            return "False"
        else:
            return "True"
        return y
    
    def get_output_example(self):
        return "answer", "<True or False>"
    