from ..base.base_task_descriptor import BaseTaskDescriptor

class CGTaskDescriptor(BaseTaskDescriptor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.use_format_suffix = False
    
    def _get_task_description(self, random_state=None):
        descriptions = [
            "Please generate a new additional column for the input table and append the new column to the right of the table. Return the new table with the additional column.",
            "Add a new extra column to the input table and place it to the right of the existing columns. Afterward, provide the updated table with the newly appended column.",
            "Create a new additional column for the input table and append it to the right. Share the modified table, which includes the new column.",
            "Please add a new column to the input table, positioning it to the right. Present the updated table with the additional column included.",
            "Generate a new supplementary column for the input table and place it on the right-hand side. Show the updated table with the added column.",
            "Extend the input table by generating a new extra column and placing it to the right. Display the resulting table with the additional column.",
            "Generate a fresh column for the input table and append it to the right side. Provide the modified table, including the newly created column.",
            "Create a new additional column for the input table and add it to the right. Share the updated table with the appended column.",
            "Please generate a new column for the input table and place it to the right. Show the updated table with the additional column.",
            "Add a newly generated column to the input table, positioning it on the right side. Present the updated table with the added column.",
            "Extend the input table by appending a new additional column to the right. Share the resulting table with the new column.",
            "Generate a new supplementary column for the input table and include it to the right. Provide the updated table with the appended column.",
            "Create a fresh column for the input table and place it on the right-hand side. Display the modified table, which contains the additional column.",
            "Add a new column to the input table and position it to the right. Show the updated table with the additional column.",
            "Please extend the input table by generating a new additional column and adding it to the right. Present the resulting table with the extra column.",
            "Generate a new column for the input table and append it on the right side. Share the updated table with the additional column.",
            "Create a new additional column for the input table and place it to the right. Provide the modified table, which includes the new column.",
            "Add a newly generated column to the input table, positioning it on the right side. Display the updated table with the appended column.",
            "Extend the input table by generating a new supplementary column and placing it on the right-hand side. Present the modified table with the added column.",
            "Generate a fresh column for the input table and add it to the right. Show the updated table with the newly created column.",
            "Please create a new additional column for the input table and append it to the right. Share the resulting table with the added column.",
            "Generate an additional new column for the input table and attach it on the right side. Afterward, return the updated table with the newly added column.",
            "Add a new supplementary column to the input table and place it on the right. Share the modified table, which includes the additional column.",
            "Please include a new column in the input table, positioning it on the right-hand side. Present the updated table with the appended column.",
            "Create a new extra column for the input table and append it to the right. Show the resulting table with the new column included.",
            "Extend the input table by generating a new additional column and placing it on the right side. Display the table with the additional column.",
            "Generate a fresh column for the input table and add it on the right. Provide the modified table, including the newly appended column.",
            "Create a new supplementary column for the input table and include it on the right. Share the updated table with the added column.",
            "Please generate a new column for the input table and place it on the right. Show the updated table with the additional column.",
            "Add a newly generated column to the input table, positioning it on the right side. Present the updated table with the new column.",
            "Extend the input table by appending a new supplementary column on the right. Share the resulting table with the additional column.",
            "Generate a new extra column for the input table and attach it to the right. Provide the updated table with the newly created column.",
            "Create a fresh column for the input table and place it on the right-hand side. Display the modified table, which includes the appended column.",
            "Add a new column to the input table and position it on the right. Show the updated table with the additional column.",
            "Please extend the input table by generating a new extra column and adding it on the right. Present the resulting table with the added column.",
            "Generate a new column for the input table and attach it on the right side. Share the updated table with the appended column.",
            "Create an additional new column for the input table and place it on the right. Provide the modified table, including the new column.",
            "Add a newly generated column to the input table, positioning it on the right side. Display the updated table with the additional column.",
            "Extend the input table by generating a new supplementary column and placing it on the right side. Present the modified table with the added column.",
            "Generate a fresh column for the input table and add it on the right. Show the updated table with the newly created column.",
            "Please create a new column for the input table and append it on the right. Share the resulting table with the new column.",
        ]
        return self.select_one_option(descriptions, random_state=random_state)

    def get_input(self, df, random_state=None):
        return self.serializer.serialize_df(df)

    # def get_output_example(self):
    #     return "updated table", "<table>"
    
    def get_output(self, y):
        return self.serializer.serialize_df(y)