from ..base.base_task_descriptor import BaseTaskDescriptor

class RETaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, page_title=None, table_title=None, **kwargs):
        super().__init__(**kwargs)
        self.page_title = page_title
        self.table_title = table_title
        
    def _get_task_description(self, random_state=None):
        descriptions = [
           f'You are given a table titled "{self.table_title}" and crawled from a web page titled "{self.page_title}". Please determine the relationship between the two columns in the table. You should only select one relationship from the candidate list. '
        ]
        return self.select_one_option(descriptions, random_state=random_state)
        
    def get_input(self, data, random_state=None):
        df, candidate_text = data
        candidate_text = "\n".join(candidate_text)

        prompt = (
            "**Candidate relationship:**\n"
            f"{candidate_text}\n\n"
            "**Table:**\n"
            f"{self.serializer.serialize_df(df)}\n"
        )
        return prompt
    
    def get_output_example(self):
        return "relationship", "<one relationship chosen from the candidate list>"
    
    def _get_output(self, y):
        return y