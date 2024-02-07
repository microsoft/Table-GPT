from ..base.base_task_descriptor import BaseTaskDescriptor

class RCFTaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, type=None, row_indices=None, columns=None, column=None, value=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.row_indices = row_indices
        self.columns = columns
        self.column = column
        self.value = value
        self.use_format_suffix = False
        
    def get_ordinal_text(self, i):
        if i == 0:
            return "first"
        if i == 1:
            return "second"
        if i == 2:
            return "third"
        if i == 3:
            return "fourth"
        if i == 4:
            return "fifth"
        if i == 5:
            return "sixth"
        if i == 6:
            return "seventh"
        if i == 7:
            return "eighth"
        if i == 8:
            return "ninth"
        if i == 9:
            return "tenth"
        raise Exception(f"Number out of scope {i}")
        
    def _get_task_description(self, random_state=None):
        if self.type == "row_projection":
            
            row_sel = ", ".join([self.get_ordinal_text(x) for x in self.row_indices]) 
            if len(self.row_indices) == 1:
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
        elif self.type == "column_projection":
            col_sel = ", ".join([f'"{x}"' for x in self.columns])
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
        elif self.type == "row_filter":
            column = f'"{self.column}"'
            value = f'"{self.value}"'
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
            raise Exception(f"Wrong type {self.type}")
        return self.select_one_option(descriptions, random_state=random_state)
        
    def get_input(self, df, random_state=None):
        return self.serializer.serialize_df(df)
    
    def get_output(self, y):
        answer = self.serializer.serialize_df(y["label"])
        
        if y["cot"] is not None:
            cot_text = y["cot"].strip()
            completion = f"{cot_text} Therefore, the final answer is: \n{answer}"
        else:
            completion = answer
        return completion
    
    # def get_output_example(self):
    #     if self.type == "column_projection":
    #         return "table", "<table with chosen columns>"
    #     else:
    #         return "table", "<table with chosen rows>"