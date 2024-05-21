from .base_table_task import BaseTableTask
import os


class RowColumnFiltering(BaseTableTask):
    def load_data_example(self, data_dir: str) -> dict:
        info = self.load_json(os.path.join(data_dir, "info.json"))
        input_table = self.load_df(os.path.join(data_dir, "input_table.csv"))
        output_table = self.load_df(os.path.join(data_dir, "output_table.csv"))
        example = {"input_table": input_table, "output_table": output_table}
        example.update(info)
        return example

    def get_ordinal_text(self, i):
        ordinal_text = {
            0: "first",
            1: "second",
            2: "third",
            3: "fourth",
            4: "fifth",
            5: "sixth",
            6: "seventh",
            7: "eighth",
            8: "ninth",
            9: "tenth",
        }
        return ordinal_text[i]

        raise Exception(f"Number out of scope {i}")

    def get_task_descriptions(self, test_example):
        task_type = test_example["task_type"]

        if task_type == "row_projection":
            row_projection_indices = test_example["row_projection_indices"]
            row_sel = ", ".join(
                [self.get_ordinal_text(x) for x in row_projection_indices]
            )
            if len(row_projection_indices) == 1:
                row_sel += " row"
            else:
                row_sel += " rows"

            descriptions = [
                f"Please select the {row_sel} in the table. Please return the table with the selected rows.",
                f"Kindly pick the {row_sel} from the table. After the selection, please provide the table with the chosen rows.",
                f"Could you choose the {row_sel} in the table? Once done, share the table with only the selected rows.",
                f"I request that you select the {row_sel} in the table. Please return the table with the specified row(s).",
                f"Please mark the {row_sel} in the table for selection. Share the table with the selected rows afterward.",
                f"I'd appreciate it if you could pick the {row_sel} from the table. Let me see the table with the chosen row(s).",
                f"If possible, select the {row_sel} in the table. Provide me with the table containing only the selected rows.",
                f"Kindly perform a selection for the {row_sel} in the table. Send me the table with the specified row(s) chosen.",
                f"I request that you choose the {row_sel} in the table. Please return the table with the selected row(s).",
                f"Could you mark the {row_sel} in the table for selection? Afterward, share the table with the chosen row(s).",
                f"Please select the {row_sel} from the table. Share the updated table containing only the selected rows.",
                f"I'd be grateful if you could mark the {row_sel} in the table for selection. Provide the table with the chosen row(s).",
                f"If possible, could you select the {row_sel} in the table? Let me know the outcome.",
                f"Kindly pick the {row_sel} from the table. Please provide the table with only the selected row(s).",
                f"I request that you perform a selection for the {row_sel} in the table. Share the updated table with the chosen row(s).",
                f"Could you choose the {row_sel} in the table? After the selection, please return the table.",
                f"Please mark the {row_sel} in the table for selection. Let me see the table with the specified row(s) chosen.",
                f"I'd appreciate it if you could select the {row_sel} in the table. Share the table with the chosen row(s) after the selection.",
                f"Kindly perform a selection for the {row_sel} in the table. Provide the modified table with the specified row(s).",
                f"I request that you mark the {row_sel} in the table for selection. Once done, return the table with the chosen row(s).",
                f"Could you choose the {row_sel} in the table? After the selection, kindly return the table.",
            ]
        elif task_type == "column_projection":
            column_projection_columns = test_example["column_projection_columns"]
            col_sel = ", ".join([f'"{x}"' for x in column_projection_columns])
            descriptions = [
                f"Please select the column {col_sel} in the table. Please return the table with the selected columns.",
                f"Kindly pick column {col_sel} from the table. After the selection, please provide the table with the chosen columns.",
                f"Could you choose column {col_sel} in the table? Once done, share the table with only the selected columns.",
                f"I request that you select column {col_sel} in the table. Please return the table with the specified column(s).",
                f"Please mark column {col_sel} in the table for selection. Share the table with the selected columns afterward.",
                f"I'd appreciate it if you could pick column {col_sel} from the table. Let me see the table with the chosen column(s).",
                f"If possible, select column {col_sel} in the table. Provide me with the table containing only the selected columns.",
                f"Kindly perform a selection for column {col_sel} in the table. Send me the table with the specified column(s) chosen.",
                f"I request that you choose column {col_sel} in the table. Please return the table with the selected column(s).",
                f"Could you mark column {col_sel} in the table for selection? Afterward, share the table with the chosen columns.",
                f"Please select column {col_sel} from the table. Share the updated table containing only the selected columns.",
                f"I'd be grateful if you could mark column {col_sel} in the table for selection. Provide the table with the chosen column(s).",
                f"If possible, could you select column {col_sel} in the table? Let me know the outcome.",
                f"Kindly pick column {col_sel} from the table. Please provide the table with only the selected column(s).",
                f"I request that you perform a selection for column {col_sel} in the table. Share the updated table with the chosen column(s).",
                f"Could you choose column {col_sel} in the table? After the selection, please return the table.",
                f"Please mark column {col_sel} in the table for selection. Let me see the table with the specified column(s) chosen.",
                f"I'd appreciate it if you could select column {col_sel} in the table. Share the table with the chosen columns after the selection.",
                f"Kindly perform a selection for column {col_sel} in the table. Provide the modified table with the specified column(s).",
                f"I request that you mark column {col_sel} in the table for selection. Once done, return the table with the chosen columns.",
                f"Could you choose column {col_sel} in the table? After the selection, kindly return the table.",
            ]
        elif task_type == "row_filter":
            row_filter_column = test_example["row_filter_column"]
            row_filter_value = test_example["row_filter_value"]
            column = f'"{row_filter_column}"'
            value = f'"{row_filter_value}"'
            descriptions = [
                f"Please select the row or rows with the value of column {column} equal to {value}. Please return the table with the selected rows.",
                f"Kindly choose the row or rows where the value of column {column} is equal to {value} in the table. After the selection, please provide the updated table.",
                f"Could you select the row or rows with the value of column {column} being {value} in the table? Once done, share the table with the selected rows.",
                f"I request that you pick the row or rows with column {column} equal to {value} in the table. Please return the table with the specified rows.",
                f"Please mark the row or rows in which column {column} has the value {value} in the table for selection. Share the table with the selected rows afterward.",
                f"I'd appreciate it if you could choose the row or rows with the value of column {column} as {value} in the table. Let me see the updated table.",
                f"If possible, select the row or rows that have the value {value} in column {column} in the table. Provide me with the table containing only the selected rows.",
                f"Kindly perform a selection for the row or rows with the value of column {column} equal to {value} in the table. Send me the table with the chosen rows.",
                f"I request that you choose the row or rows with the value of column {column} equal to {value} in the table. Please return the table with the selected rows.",
                f"Could you mark the row or rows with the value of column {column} as {value} in the table for selection? Afterward, share the table with the chosen rows.",
                f"Please select the row or rows where column {column} has the value {value} in the table. Share the updated table containing only the selected rows.",
                f"I'd be grateful if you could mark the row or rows with the value of column {column} equal to {value} in the table for selection. Provide the table with the chosen rows.",
                f"If possible, could you select the row or rows with the value of column {column} as {value} in the table? Let me know the outcome.",
                f"Kindly pick the row or rows with the value of column {column} equal to {value} in the table. Please provide the table with only the selected rows.",
                f"I request that you perform a selection for the row or rows with the value of column {column} equal to {value} in the table. Share the updated table with the chosen rows.",
                f"Could you choose the row or rows with the value of column {column} being {value} in the table? After the selection, please return the table.",
                f"Please mark the row or rows with the value of column {column} equal to {value} in the table for selection. Let me see the table with the specified rows chosen.",
                f"I'd appreciate it if you could select the row or rows with the value of column {column} as {value} in the table. Share the table with the chosen rows after the selection.",
                f"Kindly perform a selection for the row or rows with the value of column {column} equal to {value} in the table. Provide the modified table with the specified rows.",
                f"I request that you mark the row or rows with the value of column {column} as {value} in the table for selection. Once done, return the table with the chosen rows.",
                f"Could you choose the row or rows with the value of column {column} equal to {value} in the table? After the selection, kindly return the table.",
            ]
        else:
            raise Exception(f"Wrong type {task_type}")

        return descriptions

    def get_input(self, test_example):
        return self.serialize_df(test_example["input_table"])

    def get_output(self, test_example):
        return self.serialize_df(test_example["output_table"])

    def get_output_template(self, test_example):
        return None
