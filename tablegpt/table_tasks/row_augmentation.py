from .column_augmentation import ColumnAugmentation
import pandas as pd


class RowAugmentation(ColumnAugmentation):
    def get_task_descriptions(self, test_example):
        descriptions = [
            "Please generate a new row for the input table and append it at the bottom of the table. Return the new table with the additional generated row.",
            "Generate a new row for the input table and add it to the bottom. Provide the updated table with the newly appended row.",
            "Create a new row for the input table and place it at the end. Afterward, share the modified table including the newly generated row.",
            "Please append a new row to the input table, positioning it at the bottom. Present the updated table with the additional row included.",
            "Add a newly generated row to the input table, making it the last entry. Share the updated table with the added row.",
            "Extend the input table by generating a new row and placing it at the bottom. Show the resulting table with the extra row.",
            "Generate a fresh row for the input table and append it at the end. Display the modified table, which includes the newly created row.",
            "Create a new row for the input table and add it at the bottom. Share the updated table with the newly appended row.",
            "Please add a new row to the input table and place it at the bottom. Present the updated table with the additional generated row.",
            "Append a newly created row to the input table, making it the last row. Provide the modified table, including the newly added row.",
            "Extend the input table by appending a new row to the bottom. Show the resulting table with the newly generated row included.",
            "Generate a new row for the input table and include it at the end. Share the updated table with the additional generated row.",
            "Create a fresh row for the input table and place it at the bottom. Display the modified table, which contains the newly added row.",
            "Add a new row to the input table and position it at the end. Present the updated table with the newly appended row.",
            "Please extend the input table by generating a new row and adding it at the bottom. Show the resulting table with the additional row.",
            "Generate a new row for the input table and append it at the end. Share the modified table with the newly generated row included.",
            "Create a new row for the input table and place it at the bottom. Provide the updated table, which contains the additional generated row.",
            "Add a newly generated row to the input table, making it the last entry. Display the updated table with the newly appended row.",
            "Extend the input table by generating a new row and positioning it at the bottom. Present the modified table with the additional row.",
            "Generate a fresh row for the input table and add it at the end. Share the updated table with the newly created row.",
            "Please create a new row for the input table and append it at the bottom. Show the resulting table with the newly added row.",
            "Generate a new row for the input table and add it at the bottom. Afterward, provide the updated table with the additional row.",
            "Create a new row for the input table and place it at the end. Share the modified table, which includes the newly appended row.",
            "Please append a new row to the input table, positioning it at the bottom. Present the updated table with the newly generated row.",
            "Add a newly generated row to the input table, making it the last entry. Show the updated table with the added row.",
            "Extend the input table by generating a new row and placing it at the bottom. Display the resulting table with the extra row.",
            "Generate a fresh row for the input table and append it at the end. Provide the modified table, including the newly created row.",
            "Create a new row for the input table and add it at the bottom. Share the updated table with the appended row.",
            "Please add a new row to the input table and place it at the bottom. Show the updated table with the additional generated row.",
            "Append a newly created row to the input table, making it the last row. Present the modified table, including the added row.",
            "Extend the input table by appending a new row to the bottom. Share the resulting table with the newly generated row.",
            "Generate a new row for the input table and include it at the end. Provide the updated table with the appended row.",
            "Create a fresh row for the input table and place it at the bottom. Display the modified table, which contains the added row.",
            "Add a new row to the input table and position it at the end. Show the updated table with the appended row.",
            "Please extend the input table by generating a new row and adding it at the bottom. Present the resulting table with the additional row.",
            "Generate a new row for the input table and append it at the end. Share the updated table with the appended row.",
            "Create a new row for the input table and place it at the bottom. Provide the modified table, which includes the new row.",
            "Add a newly generated row to the input table, making it the last entry. Display the updated table with the additional row.",
            "Extend the input table by generating a new row and positioning it at the bottom. Present the modified table with the added row.",
            "Generate a fresh row for the input table and add it at the end. Show the updated table with the newly created row.",
            "Please create a new row for the input table and append it at the bottom. Share the resulting table with the added row.",
        ]
        return descriptions

    def get_output(self, test_example):
        data = test_example["input_table"]
        new_row = pd.DataFrame([test_example["label"]], columns=data.columns)
        new_df = pd.concat([data, new_row], axis=0).reset_index(drop=True)
        return self.serialize_df(new_df)
