from .base_table_task import BaseTableTask
from copy import deepcopy


class DataImputation(BaseTableTask):
    def get_task_descriptions(self, test_example):
        missing_token = "[MISSING]"
        descriptions = [
            f"Please fill in the missing value in the input table. The missing value is denoted by '{missing_token}'. Please only return the value filled in. Do not return the whole table.",
            f"Kindly complete the input table by providing the value for the missing entry, indicated by '{missing_token}'. Only the filled-in value is required, not the entire table.",
            f"We request that you enter the correct value for the missing cell in the input table, marked as '{missing_token}'. Please provide only the filled-in value, not the entire table.",
            f"To proceed, fill in the blank cell within the input table. The placeholder '{missing_token}' signifies the missing value. Share only the filled-in value, not the entire table.",
            f"Your task is to fill out the input table by inserting the appropriate value where '{missing_token}' is present. Please share only the value filled in, not the complete table.",
            f"Complete the input table by entering the missing value, represented by '{missing_token}'. Only the filled-in value should be provided; the rest of the table is unnecessary.",
            f"We need you to fill in the missing entry in the input table, denoted by '{missing_token}'. Please return just the value you filled in, excluding the rest of the table.",
            f"Your responsibility is to supply the missing value in the input table marked as '{missing_token}'. Provide only the value filled in, not the entire table content.",
            f"Please ensure the input table is complete by filling in the missing data where '{missing_token}' is shown. Share only the value you added, not the entire table.",
            f"Insert the correct value into the input table, replacing '{missing_token}', which represents the missing data. Share solely the filled-in value; the complete table is unnecessary.",
            f"Kindly update the input table by adding the missing value denoted by '{missing_token}'. Provide just the value you inserted; there's no need to return the entire table.",
            f"You are accountable for providing the missing value in the input table, indicated by '{missing_token}'. Please only offer the filled-in value, excluding the entire table content.",
            f"It is your duty to provide the missing value in the input table, identified as '{missing_token}'. Kindly share only the filled-in value, not the rest of the table.",
            f"You have the responsibility to fill in the missing value in the input table, marked with '{missing_token}'. Provide solely the value you inserted, not the complete table.",
            f"You are tasked with supplying the missing data in the input table, denoted by '{missing_token}'. Please only return the filled-in value, not the whole table.",
            f"Your obligation is to enter the missing value in the input table, represented as '{missing_token}'. Share just the value you added; there's no need for the entire table.",
            f"Your job is to fill out the missing value in the input table, labeled as '{missing_token}'. Provide only the value filled in, excluding the rest of the table.",
            f"The missing value in the input table, indicated by '{missing_token}', should be supplied by you. Please only provide the value filled in, not the entire table.",
            f"You must provide the missing data in the input table, denoted with '{missing_token}'. Only the filled-in value is required, not the complete table.",
            f"Please fill in the missing value within the input table, marked as '{missing_token}'. Only the value you filled in should be given; the entire table is unnecessary.",
            f"You are required to insert the missing value into the input table, where '{missing_token}' is located. Share only the value filled in, not the entire table content.",
            f"It falls under your responsibility to complete the missing value in the input table, denoted as '{missing_token}'. Provide just the filled-in value; the rest of the table is not needed.",
            f"To fulfill your responsibility, please provide the missing value in the input table, represented by '{missing_token}'. Only the filled-in value should be provided, not the whole table.",
            f"Your task is to supply the missing value in the input table, marked with '{missing_token}'. Please share only the filled-in value, not the entire table content.",
            f"Please ensure the missing value in the input table, identified by '{missing_token}', is filled. Share only the value filled in, not the complete table.",
            f"You have been assigned the task of providing the missing data in the input table, labeled as '{missing_token}'. Only the filled-in value is necessary, not the entire table.",
            f"We expect you to fill in the missing value in the input table, denoted by '{missing_token}'. Please only provide the value filled in, not the whole table content.",
            f"Your duty is to complete the missing value in the input table, indicated by '{missing_token}'. Provide only the value filled in, excluding the rest of the table.",
            f"You are responsible for inserting the missing data in the input table, represented as '{missing_token}'. Kindly share only the filled-in value, not the entire table.",
            f"It is your responsibility to supply the missing value in the input table, marked as '{missing_token}'. Please only return the filled-in value, not the entire table content.",
            f"You are accountable for providing the missing value in the input table, identified as '{missing_token}'. Share only the value you filled in, not the rest of the table.",
            f"You have the responsibility to fill in the missing value in the input table, marked with '{missing_token}'. Only the filled-in value is required, not the complete table.",
            f"You are tasked with supplying the missing data in the input table, denoted by '{missing_token}'. Provide solely the value you inserted, not the whole table.",
            f"Your obligation is to enter the missing value in the input table, represented as '{missing_token}'. Please share just the value you added; there's no need for the entire table.",
            f"Your job is to fill out the missing value in the input table, labeled as '{missing_token}'. Only the value filled in should be given; the rest of the table is unnecessary.",
            f"The missing value in the input table, indicated by '{missing_token}', should be supplied by you. Please only provide the value filled in, not the entire table.",
            f"You must provide the missing data in the input table, denoted with '{missing_token}'. Only the filled-in value is required, not the complete table.",
            f"Please fill in the missing value within the input table, marked as '{missing_token}'. Only the value you filled in should be given; the entire table is not needed.",
            f"You are required to insert the missing value into the input table, where '{missing_token}' is located. Share only the value filled in, not the entire table content.",
            f"It falls under your responsibility to complete the missing value in the input table, denoted as '{missing_token}'. Provide just the filled-in value; the rest of the table is unnecessary.",
            f"To fulfill your responsibility, please provide the missing value in the input table, represented by '{missing_token}'. Only the filled-in value should be provided, not the whole table.",
            f"Your task is to supply the missing value in the input table, marked with '{missing_token}'. Please share only the filled-in value, not the entire table content.",
            f"Please ensure the missing value in the input table, identified by '{missing_token}', is filled. Share only the value filled in, not the complete table.",
            f"You have been assigned the task of providing the missing data in the input table, labeled as '{missing_token}'. Only the filled-in value is necessary, not the entire table.",
            f"We expect you to fill in the missing value in the input table, denoted by '{missing_token}'. Please only provide the value filled in, not the whole table content.",
            f"Your duty is to complete the missing value in the input table, indicated by '{missing_token}'. Provide only the value filled in, excluding the rest of the table.",
            f"You are responsible for inserting the missing data in the input table, represented as '{missing_token}'. Kindly share only the filled-in value, not the entire table.",
            f"It is your responsibility to supply the missing value in the input table, marked as '{missing_token}'. Please only return the filled-in value, not the entire table content.",
            f"You are accountable for providing the missing value in the input table, identified as '{missing_token}'. Share only the value you filled in, not the rest of the table.",
            f"You have the responsibility to fill in the missing value in the input table, marked with '{missing_token}'. Only the filled-in value is required, not the complete table.",
        ]
        return descriptions

    def get_input(self, test_example):
        df = test_example["input_table"]
        return self.serialize_df(df)

    def get_output(self, test_example):
        answer = str(test_example["label"])
        return self.answer_to_json("value", answer)

    def get_output_template(self, test_example):
        return self.answer_to_json("value", "<value filled in>")

    def augment_data(self, test_data_dict: dict, random_state: int) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        data_dict_perturb["input_table"] = data_dict_perturb["input_table"].sample(
            frac=1, axis=1, random_state=random_state
        )
        return data_dict_perturb
