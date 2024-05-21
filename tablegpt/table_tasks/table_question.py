from .base_table_task import BaseTableTask
import os
from copy import deepcopy


class TableQuestion(BaseTableTask):
    def get_task_descriptions(self, test_example):
        descriptions = [
            "Please look at the table, and then answer the question. Please also provide an explanation on your answer."
        ]
        return descriptions

    def load_data_example(self, data_dir) -> dict:
        info = self.load_json(os.path.join(data_dir, "info.json"))
        input_table = self.load_df(os.path.join(data_dir, "input_table.csv"))
        example = {
            "input_table": input_table,
            "label": info["label"],
            "question": info["question"],
        }
        return example

    def get_input(self, test_example):
        df = test_example["input_table"]
        question = test_example["question"]
        text = "*Table*\n" f"{self.serialize_df(df)}" "*Question:*\n" f"{question}"
        return text

    def get_output(self, test_example):
        return self.answer_to_json("answer", test_example["label"])

    def get_output_template(self, test_example):
        return self.answer_to_json("answer", "<YOUR ANSWER>")

    def shorten_data(self, test_data_dict):
        test_data_dict = deepcopy(test_data_dict)
        df_test = test_data_dict["input_table"]

        if df_test.shape[1] < 2:
            return test_data_dict

        # drop the longest column
        df_test_short = self.drop_long_column(df_test)
        test_data_dict["input_table"] = df_test_short

        return test_data_dict

    def drop_long_column(self, df):
        max_c = None
        max_length = float("-inf")

        for c in df.columns:
            length = sum([len(str(x)) for x in df[c].values])
            if length > max_length:
                max_c = c
                max_length = length

        new_columns = [c for c in df.columns if c != max_c]
        return df[new_columns]
