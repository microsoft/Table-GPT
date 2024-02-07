from ..base.base_task_descriptor import BaseTaskDescriptor
from copy import deepcopy

class HVMTaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Given the input table data and the list of candidate headers, please determine the most suitable column header for each column in the table. Please only choose column headers from the candidate list. Please only return the most suitable column header for each column. Return the chosen column headers in a list. Do not return the entire table.",
            "Using the provided table data and the list of potential headers, select the appropriate header for each column in the input table. Only utilize headers from the candidate list, and ensure that you return only the most fitting header for each column. Provide the selected column headers in a list format.",
            "Evaluate the given table information alongside the list of potential headers. Your task is to decide the most fitting column header for each individual column present in the table. Utilize only the headers listed as candidates, and make sure to offer only the most suitable header for each column. Present the chosen column headers within a list.",
            "Based on the input table data and the list of headers under consideration, make a determination about the optimal header for every column within the table. Utilize solely the headers present in the candidate list. Your output should include only the most appropriate column headers, organized in the form of a list.",
            "Examine the input table data and the list of possible headers provided. Your objective is to select the most appropriate header for each individual column that exists in the table. Choose headers exclusively from the candidate list, and ensure that you provide a list containing only the selected column headers.",
            "Analyze the table data given and the list of potential headers. Your task involves identifying the most suitable column header for each and every column in the table. Use only the column headers listed among the candidates, and deliver the chosen column headers presented in the shape of a list.",
            "Given access to the input table data and a list containing candidate headers, your task is to determine the most fitting header for each column within the table. Limit your selection to headers found in the candidate list, and produce a list that includes only the chosen column headers.",
            "Assess both the input table data and the available list of candidate headers. Your goal is to select the most appropriate header for each column existing within the table. Solely choose column headers from the provided candidate list, and ensure that your output consists solely of the chosen column headers, organized into a list.",
            "Upon reviewing the input table data alongside the list of potential headers, decide on the most suitable header for every column present in the table. Choose exclusively from the candidate headers list and provide a list containing only the selected column headers.",
            "Examine the input table data and the list of headers that can be considered. Your task is to identify the most fitting column header for each individual column present in the table. Only select column headers from the candidate list, and present the chosen column headers as a list.",
            "Utilize the provided table data and the list of headers that are candidates. Determine the most suitable header for each column in the table, selecting only from the candidate headers list. Share the chosen column headers within a list format.",
            "Given the input table data and a list of potential headers, make decisions about the most appropriate column header for each table column. Choose your headers solely from the list of candidates, and provide the selected column headers in the form of a list.",
            "Analyze the input table data alongside the list of possible headers. Your objective is to find the most suitable header for each individual column within the table. Select column headers exclusively from the list of candidates, and present the chosen column headers in the shape of a list.",
            "Review the provided input table data and the list of headers under consideration. Your task is to determine the most fitting column header for every column present in the table. Use only the candidate headers and provide the chosen column headers in list form.",
            "Given the input table data and the list of headers that are potential candidates, your role is to choose the most suitable header for each column in the table. Choose exclusively from the candidate headers list and provide the selected column headers as a list.",
            "Evaluate the input table data and the list of possible headers available. Your responsibility involves deciding on the most appropriate column header for each table column. Limit your choices to the headers listed as candidates, and present the chosen column headers in list format.",
            "Based on the input table data and the list of headers in consideration, make determinations about the most suitable column header for each table column. Choose headers only from the candidate list and provide the selected column headers in the form of a list.",
            "Examine the provided input table data along with the list of potential headers. Your goal is to identify the most fitting header for each column within the table. Only consider column headers from the candidate list, and present the chosen headers in the shape of a list.",
            "Using the input table data and the list of headers that are candidates, determine the most suitable header for each table column. Make your choices solely from the list of candidate headers, and provide the selected column headers in list form.",
            "Review the input table data and the list of headers that are possible options. Your task is to choose the most appropriate header for each column in the table. Choose exclusively from the candidate headers list and present the selected column headers in list format.",
            "Given the input table data and a list of potential headers, your role is to identify the most fitting header for every column in the table. Choose your headers solely from the list of candidates, and provide the selected column headers as a list.",
            "With the input table data and the list of potential headers, identify the best-fitting column header for each table column using only the candidate headers. Provide the optimal column header for each column, presenting them in a list.",
            "Utilizing the input table data and the roster of feasible headers, ascertain the most appropriate column header for every table column. Select column headers exclusively from the list of candidates, and furnish the chosen ones in a list format.",
            "Given the input table data and the array of possible headers, deduce the most fitting column header for each table column. Employ solely the candidate headers, and compile the selected column headers in list form.",
            "Analyze the input table data along with the available header options, and decide on the best-matching column header for each individual column in the table. Limit your choices to the candidate headers, and present the chosen column headers in a list.",
            "Based on the input table data and the selection of potential headers, opt for the most suitable column header for each table column. Restrict your choices to the provided candidates, and organize the selected column headers into a list.",
            "When provided with the input table data and a list of potential headers, determine the most fitting column header for every column within the table. Use only the headers from the candidate list and return your selections in the form of a list.",
            "Given the input table data and the available header choices, ascertain the most appropriate column header for each table column. Choose the column headers exclusively from the list of candidates and arrange them in a list.",
            "Utilize the input table data and the roster of possible headers to identify the optimal column header for each table column. Consider only the candidate headers and present the chosen ones in list format.",
            "Evaluate the input table data and the provided headers, then decide on the most suitable column header for each column in the table. Choose from the candidate headers exclusively and present them as a list.",
            "With the input table data and the list of potential headers at hand, make determinations about the most fitting column header for every table column. Only select column headers from the candidate list and compile them into a list.",
            "Given the input table data and the assortment of candidate headers, deduce the most appropriate column header for each table column. Choose column headers solely from the candidate list, and collect them in a list format.",
            "Analyze the input table data along with the provided headers, and identify the most suitable column header for each column in the table. Select the column headers exclusively from the candidate list, and arrange them as a list.",
            "When presented with the input table data and the list of potential headers, determine the most suitable column header for each table column. Base your choices only on the candidate headers, and present the chosen column headers in a list.",
            "Given the input table data and the available candidate headers, find the most fitting column header for each column in the table. Choose column headers exclusively from the provided candidates and organize them in a list.",
            "Utilize the input table data and the array of potential headers to pinpoint the optimal column header for each table column. Rely solely on the candidate headers and display the chosen column headers in list form.",
            "Evaluate the input table data and the assortment of possible headers, then select the most appropriate column header for each table column. Choose from the list of candidate headers only and compile them into a list.",
            "With the input table data and the provided headers, ascertain the most fitting column header for each column within the table. Utilize only the candidate headers and present the chosen column headers in a list.",
            "Given the input table data and the list of potential headers, deduce the most suitable column header for each table column. Choose column headers exclusively from the candidates provided and arrange them in a list format.",
            "Analyze the input table data along with the available headers, and decide on the most appropriate column header for each column in the table. Base your choices solely on the candidate headers and present them as a list.",
            "When presented with the input table data and the assortment of candidate headers, identify the most fitting column header for each table column. Choose column headers only from the list of candidates and collect them in a list.",
        ]
        return self.select_one_option(descriptions, random_state=random_state)
    
    def get_input(self, df, random_state=None):
        candidate_text = []
        for c in df.columns:
            candidate_text.append(f"- {c}")
        candidate_text = "\n".join(candidate_text)
        df_no_header = deepcopy(df)
        df_no_header.columns = ["" for _ in range(df.shape[1])]
        
        prompt = (
            "**Table Data:**\n"
            f"{self.serializer.serialize_df(df_no_header)}\n"
            "**Candidate column headers:**\n"
            f"{candidate_text}\n"
        )
        return prompt
    
    def _get_output(self, y):
        return y
    
    def get_output_example(self):
        return "column_headers", "<a list of headers for each column chosen from the candidate list>"