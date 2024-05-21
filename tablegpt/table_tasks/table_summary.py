from .base_table_task import BaseTableTask


class TableSummary(BaseTableTask):
    def get_task_descriptions(self, test_example):
        descriptions = [
            "Please look at the table below and provide a title for the table.",
            "Kindly refer to the table below and suggest a suitable title for it.",
            "I'd appreciate it if you could glance at the table and offer a title for it.",
            "Could you spare a moment to look at the table and give it an appropriate title?",
            "Your task is to review the table and come up with a title for it.",
            "Given the table below, could you provide a title that accurately represents its contents?",
            "Here's a table for your consideration; please suggest a title that fits its contents.",
            "I request that you provide a summary of the input table's content.",
            "Kindly give a concise overview of what the input table represents.",
            "Take a moment to summarize the key points of the input table.",
            "Your task is to give a summary of the input table's main information.",
            "Could you spare a moment to summarize the input table's key findings?",
            "I'd appreciate it if you could provide a summary of the input table after examining it.",
            "Given the input table, can you provide a summary that captures its main data?",
            "Here's an input table for your consideration; please offer a summary of its key aspects.",
            "After reviewing the input table, could you provide a brief summary of its main points?",
            "I'd like your input on this table – can you summarize its contents for me?",
            "Please take a look at the input table and provide a concise summary of its data.",
            "Your help is needed in summarizing the input table and its main information.",
            "Summarize the input table and its key details for easy understanding.",
            "Your task is to analyze the input table and provide a summary of its main aspects.",
            "Could you please glance at the input table and offer a summary that captures its essence?",
            "Please provide a summary for the input table after reviewing its contents.",
            "Your input is valued – kindly summarize the input table's data.",
            "Having looked at the input table, can you give a summary that reflects its main points?",
            "Here's an input table that needs summarizing; can you do that for me?",
            "After considering the input table, please provide a summary that best represents it.",
            "I request that you review the table below and give a brief summary of its contents.",
            "Kindly examine the table and provide a concise overview of what it represents.",
            "Take a moment to look at the table and summarize its key points.",
            "Your task is to glance at the table and provide a summary of its contents.",
            "Could you spare a moment to review the table and give a summary of its main information?",
            "I'd appreciate it if you could summarize the table's content after looking at it.",
            "Given the table below, can you provide a summary that captures its main data?",
            "Here's a table for your consideration; please offer a summary of its key findings.",
            "After examining the table, could you provide a brief summary of its main points?",
            "Please take a look at the table and provide a concise summary of its data.",
            "Your help is needed in summarizing the table below and its main information.",
            "Summarize the table and its key details for easy understanding.",
            "Your task is to analyze the table and provide a summary of its main aspects.",
            "Could you please glance at the table and offer a summary that captures its essence?",
            "Please provide a summary for the table after reviewing its contents.",
            "Having looked at the table, can you give a summary that reflects its main points?",
            "Here's a table that needs summarizing; can you do that for me?",
            "After considering the table, please provide a summary that best represents it.",
        ]
        return descriptions

    def get_input(self, test_example):
        return self.serialize_df(test_example["input_table"])

    def get_output(self, test_example):
        return self.answer_to_json("summary", test_example["label"])

    def get_output_template(self, test_example):
        return self.answer_to_json("summary", "<summary of table>")
