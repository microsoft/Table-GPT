from ..base.base_task_descriptor import BaseTaskDescriptor
import json

class CTATaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        description = "Please look at the input column and determine the semantic type that can describe *every single* instance the input column. Please only choose one semantic type from the candidate list, and remember that the type you choose has to accurately describe every single entity in the column. If no candidate column type can suitably describe every single instance in the column, please return 'None'. Please only choose one type from the candidate list below, and *do not* create new types."
        return description
    
    def get_input(self, data, random_state=None):
        df, candidate_text = data
        candidate_text = "\n".join(candidate_text)

        prompt = (
            "**Column:**\n"
            f"{self.serializer.serialize_df(df)}\n"
            "**Candidate column type:**\n"
            f"{candidate_text}\n"
        )
        return prompt
    
    def get_output_example(self):
        return "chosen_semantic_type", "<an entry from the candidate list or None>"
    
    def _get_output(self, y):
        if y is None:
            return "None"
        else:
            return y[0]
    