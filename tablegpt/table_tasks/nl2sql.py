from .base_table_task import BaseTableTask
import os


class NL2SQL(BaseTableTask):
    def get_task_descriptions(self, test_example):
        descriptions = [
            "Please write the SQL query given the input table and question. Use 'table' as the table name if needed.",
            "Could you create the SQL query using the input table and question, possibly with 'table' as the table name?",
            "Your task is to generate an SQL query using the input table and question. Feel free to employ 'table' as the table name.",
            "Compose the SQL query based on the input table and question. In case it's necessary, utilize 'table' as the table name.",
            "Please come up with an SQL query by referring to the input table and question. You can insert 'table' as the table name if required.",
            "Your job is to write an SQL query while considering the input table and question. Use 'table' as the table name if it helps.",
            "Given the input table and question, devise an SQL query. Include 'table' as the table name if it makes the query clearer.",
            "Create an SQL query with the input table and question in mind. Incorporate 'table' as the table name whenever appropriate.",
            "Design an SQL query using the input table and question as the basis. 'Table' can be used as the table name if necessary.",
            "Please generate an SQL query by using the provided input table and question. You may employ 'table' as the table name if it makes the query more understandable.",
            "Your task is to come up with an SQL query with reference to the input table and question. You can utilize 'table' as the table name when needed.",
            "Compose the SQL query based on the input table and question given. Feel free to include 'table' as the table name for clarity.",
            "Please write an SQL query using the input table and question. If needed, use 'table' as the table name.",
            "Your job is to create an SQL query using the input table and question as the reference. Use 'table' as the table name if it improves the query's readability.",
            "Given the input table and question, devise an SQL query. In case it helps, employ 'table' as the table name in the query.",
            "Develop an SQL query with the input table and question in mind. Don't forget to consider using 'table' as the table name if appropriate.",
            "Design an SQL query based on the input table and question. Incorporate 'table' as the table name if it makes the query more understandable.",
            "Please generate an SQL query by referring to the input table and question provided. 'Table' can be used as the table name if necessary.",
            "Your task is to come up with an SQL query using the input table and question as a guide. You may utilize 'table' as the table name when needed.",
            "Compose the SQL query based on the input table and question given. If needed, include 'table' as the table name for clarity.",
            "Please write an SQL query using the input table and question provided. If necessary, use 'table' as the table name.",
            "Given the input table and question, please draft an SQL query. If required, employ 'table' as the table name.",
            "Create an SQL query based on the input table and question. You can use 'table' as the table name if it aids understanding.",
            "Compose the SQL query using the input table and question provided. Feel free to insert 'table' as the table name, if appropriate.",
            "Please write the SQL query for the given input table and question. Consider using 'table' as the table name when necessary.",
            "Your task is to generate an SQL query using the input table and question as guidance. Use 'table' as the table name if it helps.",
            "Given the input table and question, devise an SQL query. You may include 'table' as the table name for clarity.",
            "Create an SQL query with reference to the input table and question. Incorporate 'table' as the table name whenever suitable.",
            "Design an SQL query based on the input table and question. 'Table' can be used as the table name if needed.",
            "Please generate an SQL query using the input table and question provided. You can employ 'table' as the table name if it improves readability.",
            "Your job is to come up with an SQL query using the input table and question as a basis. You may use 'table' as the table name when appropriate.",
            "Compose the SQL query based on the input table and question given. If necessary, include 'table' as the table name for better understanding.",
            "Please write an SQL query using the input table and question. If needed, utilize 'table' as the table name.",
            "Your task is to create an SQL query using the input table and question as a reference. Use 'table' as the table name if it aids comprehension.",
            "Given the input table and question, devise an SQL query. Consider using 'table' as the table name in the query if it facilitates clarity.",
            "Develop an SQL query with the input table and question in mind. Don't forget to consider using 'table' as the table name if applicable.",
            "Design an SQL query based on the input table and question. Incorporate 'table' as the table name if it enhances the query's readability.",
            "Please generate an SQL query by referring to the input table and question provided. You may use 'table' as the table name if necessary.",
            "Your task is to come up with an SQL query using the input table and question as a guide. You can utilize 'table' as the table name when required.",
            "Compose the SQL query based on the input table and question given. If needed, add 'table' as the table name for clarity.",
            "Please write an SQL query using the input table and question provided. If required, use 'table' as the table name.",
        ]
        return descriptions

    def get_input(self, test_example):
        df = test_example["input_table"]
        question = test_example["question"]
        df_text = self.serialize_df(df)
        text = "**Input table:**\n" f"{df_text}\n" f"**Question:**\n{question}\n"
        return text

    def get_output(self, test_example):
        return self.answer_to_json("SQL", test_example["label"])

    def get_output_template(self, test_example):
        return self.answer_to_json("SQL", "<SQL code>")
