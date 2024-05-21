from .base_table_task import BaseTableTask
from copy import deepcopy


class ErrorDetection(BaseTableTask):
    def get_task_descriptions(self, test_example):
        descriptions = [
            "Please examine the input table and let me know which cell or cells are erroneous. If there are multiple erroneous cells, return them all in a list. If there is no erroneous cell, return 'None'. Please only return the erroneous cell or cells with high confidence.",
            "Kindly review the provided input table and inform me of any incorrect cell(s). Should there be more than one mistaken cell, provide a list of all. If no cell is incorrect, state 'None'. Please share only confidently identified erroneous cell(s).",
            "Take a look at the input table and indicate any cells that contain errors. If there are several cells with errors, present them in a list. If no cells have errors, state 'None'. Only report cells with high confidence of being erroneous.",
            "I request an analysis of the input table to identify any flawed cell(s). Should multiple cells be flawed, list them. In the absence of flawed cells, mention 'None'. Report only those cells with high confidence in their error status.",
            "Please inspect the input table and let me know about any incorrect cell(s). If there are multiple cells with errors, list them all. In the absence of errors, state 'None'. Only provide cells deemed erroneous with high confidence.",
            "Kindly examine the input table and indicate any cell(s) that are inaccurate. Should there be more than one inaccurate cell, provide a list. If no cell is inaccurate, respond with 'None'. Share only those erroneous cell(s) for which you have high confidence.",
            "Review the input table and notify me of any cells that are mistaken. If there are multiple erroneous cells, list them. If no cells are erroneous, reply with 'None'. Share only the cells with a high level of confidence in their error status.",
            "I need you to analyze the input table and highlight any cell(s) containing errors. If there are multiple cells with errors, compile them into a list. If no cells have errors, state 'None'. Present only the cells with a strong confidence of being erroneous.",
            "Please assess the input table and inform me of any incorrect cell(s). If you find more than one erroneous cell, provide a list of them all. If there are no erroneous cells, indicate 'None'. Share only the erroneous cell(s) where your confidence is high.",
            "Take a look at the input table and let me know about any cells that are incorrect. Should there be multiple cells with errors, gather them in a list. If there are no erroneous cells, say 'None'. Provide only the cells you are highly confident are erroneous.",
            "I would appreciate it if you could examine the input table and identify any erroneous cell(s). If there happen to be several erroneous cells, create a list of them. In case no cells are erroneous, mention 'None'. Only share the cells that you confidently consider as erroneous.",
            "Kindly review the input table and let me know about any cell or cells that have errors. If there are multiple cells with mistakes, display them in the form of a list. If no cells are erroneous, indicate 'None'. Only communicate the erroneous cell(s) when your confidence is high.",
            "Please go through the input table and detect any cell or cells that are erroneous. If you come across multiple erroneous cells, compile a list. If there are no erroneous cells, provide 'None'. Limit your response to cells that you are confident are erroneous.",
            "I request an examination of the input table to identify any cell or cells with errors. Should multiple cells contain errors, compile them into a list. If no cells contain errors, reply with 'None'. Share only those cells for which you have a high level of confidence in their error status.",
            "Take a moment to examine the input table and let me know which cell or cells contain errors. If there are multiple erroneous cells, gather them in a list. If no cells are erroneous, indicate 'None'. Please only provide the erroneous cell or cells that you are highly confident about.",
            "Kindly analyze the input table and notify me of any cell or cells that are erroneous. If multiple cells are found to be erroneous, list them out. If no cells are erroneous, mention 'None'. Share only the erroneous cell or cells for which you possess a high degree of confidence.",
            "Please carefully inspect the input table and inform me about any cell or cells that are incorrect. Should there be multiple incorrect cells, compile a list of them. If no cells are incorrect, reply with 'None'. Present only those cells for which you have strong confidence in their error status.",
            "I need you to review the input table and identify any cell or cells that are in error. If there are multiple cells with errors, create a list of them. If no cells have errors, state 'None'. Share only the cells that you are highly confident are erroneous.",
            "Please evaluate the input table and point out any erroneous cell or cells. If there are multiple erroneous cells, list them for me. If there are no erroneous cells, state 'None'. Only provide the cells that you have a high level of confidence in their error status.",
            "Kindly go through the input table and inform me about any cell or cells that are incorrect. Should there be multiple incorrect cells, compile a list. If no cells are incorrect, respond with 'None'. Share only the cells that you are highly confident are erroneous.",
            "Take a careful look at the input table and indicate any cell or cells that contain errors. If there are multiple cells with errors, compile them into a list. If no cells have errors, state 'None'. Please only share the erroneous cell or cells where you have a high level of confidence.",
            "Kindly assess the input table and inform me about any cell or cells that are flawed. If there are multiple flawed cells, list them. If no cells are flawed, state 'None'. Share only the cells that you are highly confident are flawed.",
            "Please examine the input table and let me know which cell or cells have mistakes. If there are multiple cells with mistakes, provide them in a list. If no cells have mistakes, respond with 'None'. Only return the cells that you have a high level of confidence in their error status.",
            "I would appreciate it if you could review the input table and identify any cell or cells with inaccuracies. If there are multiple cells with inaccuracies, compile a list of them. If no cells have inaccuracies, mention 'None'. Only share the cells that you are highly confident are inaccurate.",
            "Take a careful look at the input table and let me know about any cell or cells that are erroneous. If there are multiple erroneous cells, compile them into a list. If no cells are erroneous, state 'None'. Share only the erroneous cell or cells where you have strong confidence.",
            "Kindly analyze the input table and inform me about any cell or cells that contain errors. If there are multiple cells containing errors, list them. If no cells contain errors, state 'None'. Only provide the cells you have a high degree of confidence in identifying as erroneous.",
            "I request you to thoroughly inspect the input table and notify me of any cell or cells that are incorrect. Should there be multiple incorrect cells, gather them in a list. If no cells are incorrect, indicate 'None'. Please only report the incorrect cell or cells with high confidence.",
            "Please carefully review the input table and identify any cell or cells with errors. If there are multiple cells with errors, list them. If no cells have errors, respond with 'None'. Only report the cells that you are highly confident contain errors.",
            "Kindly evaluate the input table and let me know about any cell or cells that have errors. If there are multiple cells with errors, provide them in a list. If no cells have errors, indicate 'None'. Only return the cells for which you have a high level of confidence in their error status.",
            "Please conduct a thorough analysis of the input table and highlight any cell or cells that are erroneous. If there are multiple erroneous cells, list them. If no cells are erroneous, state 'None'. Share only the cells that you are highly confident are erroneous.",
            "Take a moment to examine the input table and indicate any cell or cells that contain errors. If there are multiple cells containing errors, create a list of them. If no cells contain errors, mention 'None'. Only share the cells where your confidence in their error status is high.",
            "I would like you to review the input table and let me know which cell or cells are incorrect. If there are multiple incorrect cells, provide them in a list. If no cells are incorrect, respond with 'None'. Only return the incorrect cell or cells that you are highly confident about.",
            "Please carefully assess the input table and inform me about any cell or cells that are mistaken. If there are multiple mistaken cells, list them. If no cells are mistaken, state 'None'. Only provide the cells that you have a high level of confidence are mistaken.",
            "Kindly go through the input table and identify any cell or cells that are flawed. If there are multiple flawed cells, compile them into a list. If no cells are flawed, mention 'None'. Only share the flawed cell or cells that you are highly confident about.",
            "Please take a close look at the input table and let me know about any cell or cells that have errors. If there are multiple cells with errors, gather them in a list. If no cells have errors, indicate 'None'. Only provide the cells that you are highly confident are erroneous.",
            "I request you to analyze the input table and indicate any cell or cells that are incorrect. If there are multiple incorrect cells, create a list of them. If no cells are incorrect, mention 'None'. Only report the incorrect cell or cells with high confidence.",
            "Please review the input table and notify me of any cell or cells that are mistaken. If there are multiple mistaken cells, compile them into a list. If no cells are mistaken, respond with 'None'. Only provide the mistaken cell or cells that you are highly confident about.",
            "Kindly assess the input table and inform me about any cell or cells that have mistakes. If there are multiple cells with mistakes, provide them in a list. If no cells have mistakes, state 'None'. Only return the cells that you are highly confident are mistaken.",
            "Please carefully examine the input table and identify any cell or cells with inaccuracies. If there are multiple cells with inaccuracies, list them. If no cells have inaccuracies, indicate 'None'. Only share the cells that you are highly confident are inaccurate.",
            "Take a moment to review the input table and let me know about any cell or cells that are incorrect. If there are multiple incorrect cells, provide them in a list. If no cells are incorrect, respond with 'None'. Only return the incorrect cell or cells that you are highly confident about.",
            "I would appreciate it if you could carefully inspect the input table and highlight any cell or cells that contain errors. If there are multiple cells containing errors, create a list of them. If no cells contain errors, mention 'None'. Only share the cells where your confidence in their error status is high.",
        ]
        return descriptions

    def get_input(self, test_example):
        df = test_example["input_table"]
        return self.serialize_df(df)

    def get_output(self, test_example):
        label = test_example["label"]
        return self.answer_to_json("erroneous_cells", str(label))

    def get_output_template(self, test_example):
        return self.answer_to_json(
            "erroneous_cells", "<a list of erroneous cells or None>"
        )

    def augment_data(self, test_data_dict: dict, random_state: int) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        data_dict_perturb["input_table"] = data_dict_perturb["input_table"].sample(
            frac=1, axis=1, random_state=random_state
        )
        return data_dict_perturb
