from .base_table_task import BaseTableTask
import os


class ColumnFinding(BaseTableTask):
    def get_task_descriptions(self, test_example):
        descriptions = [
            f"Please look at the table below and find the column that contains the given cell value."
        ]
        return descriptions

    def load_data_example(self, data_dir) -> dict:
        info = self.load_json(os.path.join(data_dir, "info.json"))
        df = self.load_df(os.path.join(data_dir, "input_table.csv"))
        example = {"input_table": df, "value": info["value"], "label": info["label"]}
        return example

    def get_input(self, test_example):
        df = test_example["input_table"]
        cell_value = test_example["value"]

        prompt = (
            "**Input Table:**\n"
            f"{self.serialize_df(df)}\n"
            "**Given Cell Value:**\n"
            f"{cell_value}\n"
        )
        return prompt

    def get_output(self, test_example):
        label = str(test_example["label"])
        return self.answer_to_json("result", label)

    def get_output_template(self, test_example):
        return self.answer_to_json(
            "result", "<name of the column containing the given cell value>"
        )
