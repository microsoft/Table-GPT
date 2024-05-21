from .base_table_task import BaseTableTask


class MissingValueIdentification(BaseTableTask):
    def get_task_descriptions(self, test_example):
        if test_example["direction"] == "row":
            descriptions = [
                "Please check the following table, there is one and exactly one cell in the table that is missing. When you find this missing cell, please point it out using the row id shown in the first column."
            ]
        else:
            descriptions = [
                "Please check the following table, there is one and exactly one cell in the table that is missing. When you find this missing cell, please point it out using its column name."
            ]
        return descriptions

    def get_input(self, test_example):
        input_text = self.serialize_df(test_example["input_table"])
        if test_example["remove_sep"]:
            return input_text.replace("[MISSING]|", "")
        else:
            return input_text.replace("[MISSING]", "")

    def get_output(self, test_example):
        label = str(test_example["label"])
        if test_example["direction"] == "row":
            return self.answer_to_json("row_id", label)
        else:
            return self.answer_to_json("missing_col", label)

    def get_output_template(self, test_example):
        if test_example["direction"] == "row":
            return self.answer_to_json(
                "row_id", "<row_id of the row with missing cell>"
            )
        else:
            return self.answer_to_json("missing_col", "<missing column name>")
