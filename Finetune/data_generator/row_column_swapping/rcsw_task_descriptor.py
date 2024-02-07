from ..base.base_task_descriptor import BaseTaskDescriptor

class RCSWTaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, type=None, swap_row_indices=None, swap_column=None, column=None, row_index=None, position=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.swap_row_indices = swap_row_indices
        self.swap_column = swap_column
        self.column = column
        self.row_index = row_index
        self.position = position
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
        if self.type == "row_swapping":
            r1, r2 = self.swap_row_indices
            row_1 = self.get_ordinal_text(r1)
            row_2 = self.get_ordinal_text(r2)
            descriptions = [
                f"Please swap the {row_1} row and the {row_2} row in the table. Please return the table after swapping.",
                f"Kindly exchange the {row_1} and {row_2} rows within the table. Then, provide the updated table.",
                f"Could you switch the {row_1} and {row_2} rows in the table? Afterward, share the table with the swapped rows.",
                f"I request that you perform a row swap between the {row_1} and {row_2} rows in the table. Share the modified table.",
                f"Please interchange the positions of the {row_1} and {row_2} rows in the table. Share the updated table afterward.",
                f"I'd appreciate it if you could swap the {row_1} and {row_2} rows in the table. Let me know the result.",
                f"If possible, could you switch the positions of the {row_1} and {row_2} rows in the table? I need the table with the rows swapped.",
                f"Kindly perform a row exchange between the {row_1} and {row_2} rows in the table. Provide the table with the rows swapped.",
                f"I request that you swap the {row_1} row with the {row_2} row in the table. After the swap, please return the table.",
                f"Could you switch the {row_1} row with the {row_2} row in the table? Once done, share the table with the rows swapped.",
                f"Please swap the {row_1} and {row_2} rows within the table. Share the updated table with the rows exchanged.",
                f"I'd be grateful if you could exchange the {row_1} and {row_2} rows in the table. Send me the table after the swap.",
                f"If possible, swap the positions of the {row_1} and {row_2} rows in the table. Let me know the outcome.",
                f"Kindly swap the {row_1} row with the {row_2} row in the table. Please provide the table after making the change.",
                f"I request that you perform a row swap between the {row_1} and {row_2} rows in the table. Share the updated table.",
                f"Could you switch the {row_1} and {row_2} rows in the table? Afterward, send me the table with the rows swapped.",
                f"Please interchange the positions of the {row_1} and {row_2} rows in the table. Let me see the updated table.",
                f"I'd appreciate it if you could swap the {row_1} and {row_2} rows in the table. Share the table with the swap.",
                f"Kindly perform a row exchange between the {row_1} and {row_2} rows in the table. Provide me with the modified table.",
                f"I request that you swap the {row_1} row with the {row_2} row in the table. Once done, please return the updated table.",
                f"Could you switch the {row_1} row with the {row_2} row in the table? After the swap, kindly return the table.",
            ]
            
        elif self.type == "column_swapping":
            col_1, col_2 = self.swap_column
            column1 = f'"{col_1}"'
            column2 = f'"{col_2}"'
            descriptions = [
                f"Please swap the position of column {column1} and the column {column2} in the table. Please return the table after swapping.",
                f"Kindly exchange the locations of column {column1} and column {column2} in the table. After the swap, please provide the updated table.",
                f"Could you switch the positions of column {column1} and column {column2} in the table? Once done, share the table with the swapped columns.",
                f"I request that you perform a column swap between {column1} and {column2} in the table. Please return the table after making the swap.",
                f"Please interchange the position of column {column1} with column {column2} within the table. Share the table with the columns swapped afterward.",
                f"I'd appreciate it if you could swap the position of column {column1} and column {column2} in the table. Let me see the updated table.",
                f"If possible, swap the location of column {column1} and column {column2} in the table. Provide me with the table after the swap.",
                f"Kindly perform a column exchange between {column1} and {column2} in the table. Send me the table with the columns swapped.",
                f"I request that you swap the position of column {column1} with column {column2} in the table. Please return the updated table.",
                f"Could you switch the location of column {column1} with column {column2} in the table? Afterward, share the table with the swapped columns.",
                f"Please swap the position of column {column1} and column {column2} within the table. Share the updated table with the columns exchanged.",
                f"I'd be grateful if you could exchange the position of column {column1} and column {column2} in the table. Provide the table after the swap.",
                f"If possible, could you swap the positions of column {column1} and column {column2} in the table? Let me know the outcome.",
                f"Kindly swap the location of column {column1} with column {column2} in the table. Please provide the table after the change.",
                f"I request that you perform a column swap between {column1} and column {column2} in the table. Share the updated table.",
                f"Could you switch the position of column {column1} with column {column2} in the table? After the swap, please return the table.",
                f"Please interchange the location of column {column1} and column {column2} in the table. Let me see the updated table.",
                f"I'd appreciate it if you could swap the position of column {column1} and column {column2} in the table. Share the table after the swap.",
                f"Kindly perform a column exchange between {column1} and column {column2} in the table. Provide the modified table.",
                f"I request that you swap the location of column {column1} with column {column2} in the table. Once done, return the updated table.",
                f"Could you switch the position of column {column1} with column {column2} in the table? After the swap, kindly return the table.",
            ]
        elif self.type == "row_moving":
            row_1 = self.get_ordinal_text(self.row_index)
            pos = "top" if self.position == "start" else "bottom"
            descriptions = [
                f"Please move the {row_1} row in the table to the {pos} row. Please return the updated table.",
                f"Kindly place the {row_1} row from the table at the {pos} position. After the move, please provide the updated table.",
                f"Could you move the {row_1} row in the table to the {pos} row? Once done, share the table with the row repositioned.",
                f"I request that you relocate the {row_1} row in the table to the {pos} row. Please return the table after the move.",
                f"Please shift the {row_1} row from the table to the {pos} position. Share the table with the row moved afterward.",
                f"I'd appreciate it if you could move the {row_1} row in the table to the {pos} position. Let me see the updated table.",
                f"If possible, move the {row_1} row in the table to the {pos} row. Provide me with the table after the repositioning.",
                f"Kindly perform a move operation for the {row_1} row in the table to the {pos} row. Send me the table with the row moved.",
                f"I request that you move the {row_1} row in the table to the {pos} position. Please return the updated table.",
                f"Could you shift the {row_1} row in the table to the {pos} row? Afterward, share the table with the row at the {pos}.",
                f"Please place the {row_1} row from the table at the {pos} row. Share the updated table with the row rearranged.",
                f"I'd be grateful if you could relocate the {row_1} row in the table to the {pos} position. Provide the table after the move.",
                f"If possible, could you move the {row_1} row in the table to the {pos} row? Let me know the outcome.",
                f"Kindly move the {row_1} row in the table to the {pos} position. Please provide the table after making the change.",
                f"I request that you perform a move operation for the {row_1} row in the table to the {pos} row. Share the updated table.",
                f"Could you shift the {row_1} row in the table to the {pos} position? After the move, please return the table.",
                f"Please relocate the {row_1} row in the table to the {pos} row. Let me see the updated table.",
                f"I'd appreciate it if you could move the {row_1} row in the table to the {pos} position. Share the table after the move.",
            ]
        elif self.type == "column_moving":
            pos = "leftmost" if self.position == "start" else "rightmost"
            column = f'"{self.column}"'
            descriptions = [
                f"Please move the column {column} in the table to {pos}. Please return the updated table.",
                f"Kindly shift column {column} in the table to the {pos} position. After the move, please provide the updated table.",
                f"Could you move the column {column} in the table to the {pos} position? Once done, share the table with the column rearranged.",
                f"I request that you relocate column {column} in the table to the {pos} position. Please return the table after the move.",
                f"Please place column {column} from the table to the {pos} position. Share the table with the column moved afterward.",
                f"I'd appreciate it if you could move the column {column} in the table to the {pos} position. Let me see the updated table.",
                f"If possible, move the column {column} in the table to the {pos} position. Provide me with the table after the repositioning.",
                f"Kindly perform a move operation for column {column} in the table to the {pos} position. Send me the table with the column moved.",
                f"I request that you move the column {column} in the table to the {pos} position. Please return the updated table.",
                f"Could you shift column {column} in the table to the {pos} position? Afterward, share the table with the column on the left.",
                f"Please relocate column {column} from the table to the {pos} position. Share the updated table with the column rearranged.",
                f"I'd be grateful if you could place column {column} in the table to the {pos} position. Provide the table after the move.",
                f"If possible, could you move the column {column} in the table to the {pos} position? Let me know the outcome.",
                f"Kindly move column {column} in the table to the {pos} position. Please provide the table after making the change.",
                f"I request that you perform a move operation for column {column} in the table to the {pos} position. Share the updated table.",
                f"Could you shift column {column} in the table to the {pos} position? After the move, please return the table.",
                f"Please place column {column} from the table to the {pos} position. Let me see the updated table.",
                f"I'd appreciate it if you could move the column {column} in the table to the {pos} position. Share the table after the move.",
                f"Kindly perform a move operation for column {column} in the table to the {pos} position. Provide the modified table.",
                f"I request that you shift column {column} in the table to the {pos} position. Once done, return the updated table.",
                f"Could you move the column {column} in the table to the {pos} position? After the move, kindly return the table.",
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
    #     return "table", "<updated table>"