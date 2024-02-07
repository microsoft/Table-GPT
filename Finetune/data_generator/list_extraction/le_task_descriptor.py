from ..base.base_task_descriptor import BaseTaskDescriptor

class LETaskDescriptor(BaseTaskDescriptor):
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Please transform the list below into a table with multiple columns. Please return the table using plain text. Use vertical bars (|) to separate columns and use a new line for each row.",
            "Convert the list into a table with several columns. Ensure the table is represented in plain text format. Utilize vertical bars (|) to separate columns and new lines for each row.",
            "Transform the list provided into a table comprising multiple columns. Remember to present the table using plain text, with vertical bars (|) as column separators and new lines for each row.",
            "Please change the list into a tabulated format with multiple columns. Provide the table using plain text, using vertical bars (|) to separate columns and a new line for each row.",
            "I request you to turn the given list into a table containing multiple columns. The table should be in plain text, with vertical bars (|) as column separators and a new line for every row.",
            "Kindly convert the list below into a table with multiple columns. The table must be returned using plain text, utilizing vertical bars (|) to separate columns and new lines for each row.",
            "Take the list provided and transform it into a table with several columns. The table should be in plain text format, with vertical bars (|) as column dividers and a new line for each row.",
            "Turn the following list into a table with multiple columns. Please deliver the table using plain text, employing vertical bars (|) as column separators and a new line for every row.",
            "Create a table with multiple columns based on the list below. Ensure the table is in plain text, using vertical bars (|) to separate columns and a new line for each row.",
            "I would like you to change the list into a table that contains multiple columns. Use plain text for the table representation, with vertical bars (|) as column separators and a new line for each row.",
            "Convert the provided list into a tabular format with multiple columns. The table should be returned in plain text, using vertical bars (|) as column dividers and new lines for each row.",
            "Transform the list below into a table with several columns. Provide the table in plain text, separating columns with vertical bars (|) and adding a new line for each row.",
            "Please convert the list into a table containing multiple columns. The table must be presented using plain text, with vertical bars (|) as column separators and a new line for every row.",
            "Turn the given list into a table with multiple columns. The table should be in plain text format, using vertical bars (|) to separate columns and a new line for each row.",
            "Change the list provided into a table with several columns. The table should be in plain text, with vertical bars (|) as column separators and a new line for each row.",
            "Create a table with multiple columns from the following list. Use plain text for the table representation, employing vertical bars (|) as column separators and a new line for every row.",
            "I request you to convert the list below into a tabulated format with multiple columns. The table must be in plain text, using vertical bars (|) as column dividers and new lines for each row.",
            "Convert the list into a table with several columns. The table should be in plain text format, with vertical bars (|) as column separators and a new line for each row.",
            "Transform the given list into a table containing multiple columns. Please return the table using plain text, separating columns with vertical bars (|) and adding a new line for each row.",
            "Please change the list below into a table with multiple columns. The table should be in plain text, utilizing vertical bars (|) as column separators and a new line for each row.",
            "I would like you to turn the provided list into a table with several columns. The table must be in plain text format, using vertical bars (|) as column separators and a new line for each row.",
            "Convert the given list into a tabular form with multiple columns. Use plain text to display the table, employing vertical bars (|) as column separators and a new line for each row.",
            "I request you to transform the list below into a table comprising multiple columns. The table should be presented in plain text format, using vertical bars (|) as column dividers and new lines for each row.",
            "Change the list provided into a table with several columns. The table must be represented in plain text, with vertical bars (|) separating columns and a new line for every row.",
            "Create a table with multiple columns based on the list below. The table should be in plain text, using vertical bars (|) as column separators and a new line for each row.",
            "Transform the provided list into a table with multiple columns. Please deliver the table using plain text, with vertical bars (|) as column separators and a new line for each row.",
            "Please convert the list into a table containing multiple columns. The table should be in plain text, separating columns with vertical bars (|) and adding a new line for every row.",
            "Turn the given list into a table with several columns. The table should be in plain text, utilizing vertical bars (|) as column separators and a new line for each row.",
            "Convert the list into a tabulated format with multiple columns. The table should be returned in plain text, using vertical bars (|) as column dividers and new lines for each row.",
            "I request you to change the list below into a table with multiple columns. Ensure the table is in plain text, using vertical bars (|) as column separators and a new line for each row.",
            "Convert the following list into a table with several columns. The table should be presented in plain text, with vertical bars (|) as column separators and a new line for each row.",
            "Transform the list provided into a table with multiple columns. Provide the table using plain text, separating columns with vertical bars (|) and adding a new line for each row.",
            "Create a table with multiple columns from the given list. Use plain text for the table representation, employing vertical bars (|) as column separators and a new line for every row.",
            "I would like you to convert the list below into a tabulated format with multiple columns. The table should be in plain text, with vertical bars (|) as column dividers and new lines for each row.",
            "Convert the list into a table with several columns. The table should be in plain text format, using vertical bars (|) as column separators and a new line for each row.",
            "Transform the given list into a table containing multiple columns. Please return the table using plain text, utilizing vertical bars (|) as column separators and a new line for each row.",
            "Please change the list below into a table with multiple columns. The table should be in plain text, separating columns with vertical bars (|) and adding a new line for each row.",
            "I would like you to turn the provided list into a table with several columns. The table must be in plain text format, using vertical bars (|) as column separators and a new line for each row.",
            "Convert the given list into a table with multiple columns. The table should be in plain text format, with vertical bars (|) as column separators and a new line for each row.",
            "Change the list provided into a table with several columns. The table should be in plain text, utilizing vertical bars (|) as column separators and a new line for each row.",
            "Create a table with multiple columns based on the list below. Use plain text for the table representation, with vertical bars (|) as column separators and a new line for each row.",
        ]
        return self.select_one_option(descriptions, random_state=random_state)
    
    def df_to_list(self, df):
        data = [" ".join(str(c) for c in df.columns)]
        for row in df.values:
            data.append(" ".join([str(x) for x in row]))
        return data
    
    def get_input(self, df, random_state=None):
        df_list = self.df_to_list(df)
        df_text = "\n".join([str(r) for r in df_list])
        return df_text

    def _get_output(self, y):
        return self.serializer.serialize_df(y)
    
    def get_output_example(self):
        return "table", "<table transformed from the list>" 