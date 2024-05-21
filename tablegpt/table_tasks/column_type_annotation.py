from .base_table_task import BaseTableTask
import os
import json


class ColumnTypeAnnotation(BaseTableTask):
    def get_task_descriptions(self, test_example):
        descriptions = [
            "Please look at the input column and determine the semantic type that can describe *every single* instance the input column. Please only choose one semantic type from the candidate list, and remember that the type you choose has to accurately describe every single entity in the column. If no candidate column type can suitably describe every single instance in the column, please return 'None'. Please only choose one type from the candidate list below, and *do not* create new types."
        ]
        return descriptions

    def get_input(self, test_example):
        df = test_example["input_table"]
        candidate_text = test_example["candidates"]
        candidate_text = "\n".join(candidate_text)

        prompt = (
            "**Column:**\n"
            f"{self.serialize_df(df)}\n"
            "**Candidate column type:**\n"
            f"{candidate_text}\n"
        )
        return prompt

    def get_output(self, test_example):
        y = test_example["label"]
        if y is None:
            answer = "None"
        else:
            answer = y[0]
        return self.answer_to_json("chosen_semantic_type", answer)

    def get_output_template(self, test_example):
        return self.answer_to_json(
            "chosen_semantic_type", "<an entry from the candidate list or None>"
        )
