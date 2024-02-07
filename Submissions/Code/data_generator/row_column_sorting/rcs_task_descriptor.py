from ..base.base_task_descriptor import BaseTaskDescriptor

class RCSTaskDescriptor(BaseTaskDescriptor):
    # decribe em task using natural language
    def __init__(self, type=None, ascending=None, sortby=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.ascending = ascending
        self.sortby = sortby
        self.use_format_suffix = False
        
    def _get_task_description(self, random_state=None):
        order = "ascending" if self.ascending else "descending"
        
        if self.type == "row":
            column = f'"{self.sortby}"'
            descriptions = [
                f"Please sort the table by the column {column} such that the values in this column are in alphabetically {order} order. Please return the sorted table.",
                f"Kindly arrange the table by sorting it based on column {column} in alphabetical {order} order. After the sorting, please provide the updated table.",
                f"Could you sort the table by column {column} in alphabetical {order} order? Once done, share the table with the sorted values in that column.",
                f"I request that you organize the table by sorting it using column {column} in alphabetical {order} order. Please return the table after the sorting.",
                f"Please arrange the table by sorting it based on the values in column {column} in alphabetical {order} order. Share the table with the sorted data afterward.",
                f"I'd appreciate it if you could sort the table using column {column} in alphabetical {order} order. Let me see the updated table.",
                f"If possible, sort the table by arranging it based on column {column} in alphabetical {order} order. Provide me with the table after the sorting.",
                f"Kindly perform a sorting operation on the table using column {column} in alphabetical {order} order. Send me the table with the sorted values.",
                f"I request that you sort the table by column {column} in alphabetical {order} order. Please return the table with the sorted data.",
                f"Could you arrange the table by sorting it using column {column} in alphabetical {order} order? Afterward, share the table with the sorted values.",
                f"Please sort the table by organizing it based on the values in column {column} in alphabetical {order} order. Share the updated table with the sorted data.",
                f"I'd be grateful if you could arrange the table by sorting it using column {column} in alphabetical {order} order. Provide the table after the sorting.",
                f"If possible, could you sort the table by column {column} in alphabetical {order} order? Let me know the outcome.",
                f"Kindly sort the table by arranging it based on column {column} in alphabetical {order} order. Please provide the table with the sorted data.",
                f"I request that you perform a sorting operation on the table using column {column} in alphabetical {order} order. Share the updated table with the sorted values.",
                f"Could you arrange the table by sorting it using column {column} in alphabetical {order} order? After the sorting, please return the table.",
                f"Please sort the table by organizing it based on the values in column {column} in alphabetical {order} order. Let me see the updated table.",
                f"I'd appreciate it if you could sort the table using column {column} in alphabetical {order} order. Share the table with the sorted data after the sorting.",
                f"Kindly perform a sorting operation on the table using column {column} in alphabetical {order} order. Provide the modified table with the sorted values.",
                f"I request that you arrange the table by sorting it using column {column} in alphabetical {order} order. Once done, return the table with the sorted data.",
                f"Could you sort the table by arranging it based on column {column} in alphabetical {order} order? After the sorting, kindly return the table.",
            ]
            
        else:
            descriptions = [
                f"Please sort the table by column headers such that the column headers are in alphabetically {order} order from left to right. Please return the sorted table.",
                f"Kindly arrange the table by sorting it based on column headers in alphabetical {order} order from left to right. After the sorting, please provide the updated table.",
                f"Could you sort the table by column headers in alphabetical {order} order from left to right? Once done, share the table with the sorted column headers.",
                f"I request that you organize the table by sorting it using column headers in alphabetical {order} order from left to right. Please return the table after the sorting.",
                f"Please arrange the table by sorting it based on the column headers in alphabetical {order} order from left to right. Share the table with the sorted column arrangement afterward.",
                f"I'd appreciate it if you could sort the table using column headers in alphabetical {order} order from left to right. Let me see the updated table.",
                f"If possible, sort the table by arranging it based on column headers in alphabetical {order} order from left to right. Provide me with the table after the sorting.",
                f"Kindly perform a sorting operation on the table using column headers in alphabetical {order} order from left to right. Send me the table with the sorted column headers.",
                f"I request that you sort the table by column headers in alphabetical {order} order from left to right. Please return the table with the sorted column arrangement.",
                f"Could you arrange the table by sorting it using column headers in alphabetical {order} order from left to right? Afterward, share the table with the sorted column headers.",
                f"Please sort the table by organizing it based on the column headers in alphabetical {order} order from left to right. Share the updated table with the sorted column arrangement.",
                f"I'd be grateful if you could arrange the table by sorting it using column headers in alphabetical {order} order from left to right. Provide the table after the sorting.",
                f"If possible, could you sort the table by column headers in alphabetical {order} order from left to right? Let me know the outcome.",
                f"Kindly sort the table by arranging it based on column headers in alphabetical {order} order from left to right. Please provide the table with the sorted column arrangement.",
                f"I request that you perform a sorting operation on the table using column headers in alphabetical {order} order from left to right. Share the updated table with the sorted column headers.",
                f"Could you arrange the table by sorting it using column headers in alphabetical {order} order from left to right? After the sorting, please return the table.",
                f"Please sort the table by organizing it based on the column headers in alphabetical {order} order from left to right. Let me see the updated table.",
                f"I'd appreciate it if you could sort the table using column headers in alphabetical {order} order from left to right. Share the table with the sorted column arrangement after the sorting.",
                f"Kindly perform a sorting operation on the table using column headers in alphabetical {order} order from left to right. Provide the modified table with the sorted column headers.",
                f"I request that you arrange the table by sorting it using column headers in alphabetical {order} order from left to right. Once done, return the table with the sorted column arrangement.",
                f"Could you sort the table by arranging it based on column headers in alphabetical {order} order from left to right? After the sorting, kindly return the table.",
            ]
        
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
    #     return "table", "<table after sorting>"