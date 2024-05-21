from .base_table_task import BaseTableTask
import os
from copy import deepcopy
import numpy as np


class SchemaMatching(BaseTableTask):
    def load_data_example(self, data_dir):
        info = self.load_json(os.path.join(data_dir, "info.json"))
        table1 = self.load_df(os.path.join(data_dir, "table1.csv"))
        table2 = self.load_df(os.path.join(data_dir, "table2.csv"))

        column_map = {}
        for c1, c2 in zip(info["old_headers"], info["alternative_headers"]):
            column_map[c1] = c2
        label = []

        for c in table1.columns:
            if c not in column_map:
                label.append((c, None))
            else:
                c2 = column_map[c]
                if c2 in table2.columns:
                    label.append((c, c2))
                else:
                    label.append((c, None))

        data_example = {"table1": table1, "table2": table2, "label": label}
        return data_example

    def get_task_descriptions(self, random_state=None):
        descriptions = [
            "Please identify the matching columns between Table A and Table B. For each column in Table A, specify the corresponding column in Table B. If a column in A has no corresponding column in Table B, you can map it to None. Represent each column mapping using a pair of column headers in a list, i.e., [Table A Column, Table B column or None]. Provide the mapping for each column in Table A and return all mappings in a list.",
            "Kindly find the corresponding columns in Table B that match with those in Table A. For every Table A column, indicate the related Table B column. If a Table A column has no match in Table B, you can denote it as None. Present each column pairing using a list of column headers like [Table A Column, Table B Column or None]. Furnish the mappings for all Table A columns and return them in a list",
            "Please discover the matching pairs of columns between Table A and Table B. Specify the respective columns from Table B for every column present in Table A. In case a Table A column has no corresponding match in Table B, you are allowed to assign it as None. Express each column association using a pair of headers within a list, such as [Table A Column, Table B Column or None]. Provide the complete set of mappings for Table A columns, and then provide them all in the form of a list",
            "Identify the corresponding columns in Table B that correspond to those in Table A. For each column in Table A, define the associated column in Table B. If a column in A doesn't have a corresponding column in Table B, you have the option to link it to None. Use a list containing pairs of column headers, like [Table A Column, Table B Column or None], to represent each mapping. Give the mappings for all Table A columns and compile them into a list",
            "Determine the matchings between columns in Table A and Table B. Indicate the relevant columns from Table B for each column present in Table A. If a column from Table A doesn't have a match in Table B, you can represent it as None. Use pairs of column headers in a list format, such as [Table A Column, Table B Column or None], to outline each mapping. Provide mappings for all the columns in Table A, and assemble them into a list",
            "Please find the equivalent columns in Table B that correspond to those in Table A. Specify the corresponding column in Table B for every column listed in Table A. If a column in Table A has no corresponding column in Table B, you can denote it as None. Present the column mappings using pairs of column headers in a list, like [Table A Column, Table B Column or None], for each mapping. Share the mappings for each Table A column and compile them all into a list",
            "Locate the matching pairs of columns between Table A and Table B. For each column present in Table A, state the associated column present in Table B. If a column in Table A has no corresponding match in Table B, you can tag it as None. Express each column correlation using a list format with column headers, for example, [Table A Column, Table B Column or None]. Provide the complete set of column mappings for Table A and organize them in a list",
            "Please ascertain the corresponding columns between Table A and Table B. Indicate the correlated columns in Table B for each of the columns in Table A. In instances where a column from Table A doesn't have a corresponding column in Table B, you can represent it as None. Use pairs of column headers in a list structure, like [Table A Column, Table B Column or None], to depict each mapping. Present the mappings for all the columns in Table A and compile them into a list",
            "Identify the columns in Table B that match with those in Table A. For every column in Table A, provide the corresponding column in Table B. If there's no corresponding column in Table B for a column in A, you can denote it as None. Use a list format with pairs of column headers, such as [Table A Column, Table B Column or None], to represent each mapping. List down the mappings for each column in Table A and return them as a list",
            "Find the corresponding columns between Table A and Table B. Specify the related columns in Table B for each column listed in Table A. If a column in Table A has no corresponding match in Table B, you can represent it as None. Utilize pairs of column headers within a list structure, like [Table A Column, Table B Column or None], to illustrate each mapping. Present the mappings for all the columns in Table A and compile them into a list",
            "Please determine the matching columns between Table A and Table B. State the corresponding columns in Table B for each of the columns in Table A. If a column in Table A has no counterpart in Table B, you can map it to None. Represent the mappings using a list of column headers in the format [Table A Column, Table B Column or None]. Provide the mappings for each Table A column and assemble them into a list",
            "Please identify the columns in Table B that correspond to those in Table A. Indicate the associated columns in Table B for each column present in Table A. If a column from Table A doesn't have a corresponding column in Table B, you can denote it as None. Use pairs of column headers in a list representation, like [Table A Column, Table B Column or None], to portray each mapping. Provide the mappings for all the columns in Table A and organize them into a list",
            "Discover the columns in Table B that match with those in Table A. For each column present in Table A, specify the corresponding column present in Table B. If a column in Table A doesn't have a corresponding column in Table B, you can represent it as None. Use pairs of column headers in a list format, like [Table A Column, Table B Column or None], to express each mapping. List out the mappings for each column in Table A and compile them in a list",
            "Please find the corresponding columns in Table B that align with those in Table A. Specify the related columns in Table B for every column listed in Table A. If a column in Table A doesn't have a matching column in Table B, you can map it to None. Express the mappings using pairs of column headers in the structure [Table A Column, Table B Column or None]. Provide the mappings for all the columns in Table A and aggregate them in a list",
            "Determine the matchings between columns in Table A and Table B. Indicate the corresponding columns from Table B for each column found in Table A. In cases where a column in Table A has no corresponding column in Table B, you can indicate it as None. Use pairs of column headers within a list, like [Table A Column, Table B Column or None], to outline each mapping. Present the mappings for all Table A columns and compile them into a list",
            "Please ascertain the matching pairs of columns between Table A and Table B. State the corresponding columns in Table B for every column listed in Table A. If a column in Table A has no corresponding match in Table B, you can denote it as None. Use a list structure with pairs of column headers, such as [Table A Column, Table B Column or None], to represent each mapping. Provide the mappings for each column in Table A and collate them in a list",
            "Locate the corresponding columns in Table B that match with those in Table A. For each column in Table A, provide the corresponding column in Table B. If a column in A doesn't have a corresponding column in Table B, you can map it to None. Represent the mappings using pairs of column headers in a list format, like [Table A Column, Table B Column or None]. Provide the mappings for each column in Table A and compile them into a list",
            "Find the corresponding columns between Table A and Table B. Specify the related columns in Table B for each column present in Table A. If a column in Table A has no corresponding column in Table B, you can denote it as None. Use pairs of column headers in a list structure, like [Table A Column, Table B Column or None], to depict each mapping. Present the mappings for all the columns in Table A and organize them into a list",
            "Please determine the matching columns between Table A and Table B. Indicate the corresponding columns in Table B for each column listed in Table A. If a column in Table A has no corresponding match in Table B, you can designate it as None. Express the mappings using pairs of column headers in the format [Table A Column, Table B Column or None]. Provide the mappings for each Table A column and compile them into a list",
            "Please identify the columns in Table B that correspond to those in Table A. State the associated columns in Table B for each of the columns in Table A. If a column from Table A doesn't have a matching column in Table B, you can denote it as None. Use pairs of column headers within a list representation, like [Table A Column, Table B Column or None], to portray each mapping. Provide the mappings for all the columns in Table A and organize them into a list",
            "Discover the columns in Table B that match with those in Table A. For each column in Table A, specify the corresponding column in Table B. If a column in Table A has no corresponding column in Table B, you can represent it as None. Utilize pairs of column headers in a list format, like [Table A Column, Table B Column or None], to express each mapping. Provide the mappings for each column in Table A and compile them in a list.",
        ]
        return descriptions

    def get_input(self, test_example):
        t1, t2 = test_example["table1"], test_example["table2"]
        t1_text = self.serialize_df(t1)
        t2_text = self.serialize_df(t2)
        text = f"Table A:\n" f"{t1_text}\n" f"Table B:\n" f"{t2_text}"
        return text

    def get_output(self, test_example):
        completion = []
        for c1, c2 in test_example["label"]:
            if c2 is None:
                completion.append([c1, "None"])
            else:
                completion.append([c1, c2])
        return self.answer_to_json("column_mappings", completion)

    def get_output_template(self, test_example):
        return self.answer_to_json("column_mappings", "<a list of column pairs>")

    def augment_data(self, test_data_dict, random_state) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        np.random.seed(random_state)
        t1, t2 = data_dict_perturb["table1"], data_dict_perturb["table2"]
        t1 = t1.sample(frac=1, axis=1)
        t2 = t2.sample(frac=1, axis=1)
        data_dict_perturb["table1"] = t1
        data_dict_perturb["table2"] = t2
        label_dict = {c1: c2 for c1, c2 in data_dict_perturb["label"]}
        data_dict_perturb["label"] = [(c, label_dict[c]) for c in t1.columns]
        return data_dict_perturb
