from ..base.base_task_descriptor import BaseTaskDescriptor

class TQTaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Please look at the table, and then answer the question. Please also provide an explanation on your answer."
        ]
        return self.select_one_option(descriptions, random_state=random_state)

    def get_input(self, data, random_state=None):
        df, question = data
        text = (
            "*Table*\n"
            f"{self.serializer.serialize_df(df)}"
            "*Question:*\n"
            f"{question}"
        )
        return text
    
    def _get_output(self, y):
        return y
    
    def get_output_example(self):
        return "answer", "<YOUR ANSWER>"
    