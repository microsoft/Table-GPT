from .base_table_task import BaseTableTask
import os
import json
from copy import deepcopy
import pandas as pd


class EntityMatching(BaseTableTask):
    def get_task_descriptions(self, test_example):
        topic = test_example["topic"]
        entity_1 = f"{topic} A"
        entity_2 = f"{topic} B"
        descriptions = [
            f"Please determine whether {entity_1} and {entity_2} refer to the same entity or not. Your final answer should be 'Yes' or 'No'.",
            f"Kindly ascertain whether {entity_1} and {entity_2} pertain to the identical entity or not. Provide your ultimate response as either 'Yes' or 'No'.",
            f"I request you to establish if {entity_1} and {entity_2} are referring to the same entity. State your final answer as 'Yes' or 'No'.",
            f"Please determine if {entity_1} and {entity_2} denote the same entity. Your conclusive answer should be 'Yes' or 'No'.",
            f"Could you confirm whether {entity_1} and {entity_2} point to the same entity or not? Indicate your final response as either 'Yes' or 'No'.",
            f"We need to establish if {entity_1} and {entity_2} represent the same entity. Provide your ultimate answer as 'Yes' or 'No'.",
            f"I would like you to determine whether {entity_1} and {entity_2} are referring to the same entity or not. Please respond with 'Yes' or 'No'.",
            f"It is essential to ascertain if {entity_1} and {entity_2} refer to the same entity. Your final response should be 'Yes' or 'No'.",
            f"Please verify whether {entity_1} and {entity_2} are denoting the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Let's determine if {entity_1} and {entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to confirm whether {entity_1} and {entity_2} represent the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Could you establish if {entity_1} and {entity_2} are referring to the same entity or not? Indicate your final response as either 'Yes' or 'No'.",
            f"We need to verify if {entity_1} and {entity_2} denote the same entity. Provide your ultimate answer as 'Yes' or 'No'.",
            f"I would like you to ascertain whether {entity_1} and {entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"It is crucial to determine if {entity_1} and {entity_2} represent the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Please confirm whether {entity_1} and {entity_2} are denoting the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Let's verify if {entity_1} and {entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to establish whether {entity_1} and {entity_2} represent the same entity or not. Indicate your final response as either 'Yes' or 'No'.",
            f"Could you determine if {entity_1} and {entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to ascertain if {entity_1} and {entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
            f"I would like you to verify whether {entity_1} and {entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"Please determine whether {entity_1} and {entity_2} refer to the same entity or not. Your final answer should be 'Yes' or 'No'.",
            f"I request you to establish if {entity_1} and {entity_2} denote the same entity. State your final answer as 'Yes' or 'No'.",
            f"Could you confirm whether {entity_1} and {entity_2} point to the same entity or not? Indicate your final response as either 'Yes' or 'No'.",
            f"We need to establish if {entity_1} and {entity_2} represent the same entity. Provide your ultimate answer as 'Yes' or 'No'.",
            f"I would like you to determine whether {entity_1} and {entity_2} are referring to the same entity or not. Please respond with 'Yes' or 'No'.",
            f"It is essential to ascertain if {entity_1} and {entity_2} refer to the same entity. Your final response should be 'Yes' or 'No'.",
            f"Please verify whether {entity_1} and {entity_2} are denoting the same entity or not. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Let's determine if {entity_1} and {entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to confirm whether {entity_1} and {entity_2} represent the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Could you establish if {entity_1} and {entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to verify if {entity_1} and {entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
            f"I would like you to ascertain whether {entity_1} and {entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"It is crucial to determine if {entity_1} and {entity_2} represent the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Please confirm whether {entity_1} and {entity_2} are denoting the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Let's verify if {entity_1} and {entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to establish whether {entity_1} and {entity_2} represent the same entity or not. Indicate your final response as either 'Yes' or 'No'.",
            f"Could you determine if {entity_1} and {entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to ascertain if {entity_1} and {entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
            f"I would like you to verify whether {entity_1} and {entity_2} are referring to the same entity or not. Your final response should be 'Yes' or 'No'.",
            f"It is essential to determine if {entity_1} and {entity_2} refer to the same entity. Indicate your conclusive answer as either 'Yes' or 'No'.",
            f"Please verify whether {entity_1} and {entity_2} are denoting the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Let's determine if {entity_1} and {entity_2} pertain to the same entity or not. Your ultimate answer should be 'Yes' or 'No'.",
            f"I request you to confirm whether {entity_1} and {entity_2} represent the same entity or not. Please respond with 'Yes' or 'No'.",
            f"Could you establish if {entity_1} and {entity_2} are referring to the same entity or not? Provide your ultimate answer as 'Yes' or 'No'.",
            f"We need to verify if {entity_1} and {entity_2} denote the same entity. Your final response should be 'Yes' or 'No'.",
        ]
        return descriptions

    def get_input(self, test_example):
        row_l = test_example["row_l"]
        row_r = test_example["row_r"]
        l_text = self.serialize_row(row_l)
        r_text = self.serialize_row(row_r)
        topic = test_example["topic"]
        entity_1 = f"{topic} A"
        entity_2 = f"{topic} B"
        text = f"{entity_1} is:\n{l_text}\n{entity_2} is:\n{r_text}"
        return text

    def get_output_template(self, test_example):
        return self.answer_to_json("answer", "<Yes or No>")

    def get_output(self, test_example):
        if test_example["label"] == "1":
            answer = "Yes"
        elif test_example["label"] == "0":
            answer = "No"
        else:
            raise Exception(f"invalid label {test_example['label']}")
        return self.answer_to_json("answer", answer)

    def load_datasets(self, task_data_dir, n_jobs=1, max_size=None, random_state=1):
        if task_data_dir.rstrip("/").endswith("train"):
            mode = "train"
        elif task_data_dir.rstrip("/").endswith("test"):
            mode = "test"
        else:
            raise Exception(
                "cannot identify mode for entity matching from task data dir"
            )

        datasets = []
        if os.path.exists(task_data_dir):
            for dataset in sorted(os.listdir(task_data_dir)):
                left = self.load_df(os.path.join(task_data_dir, dataset, "tableA.csv"))
                right = self.load_df(os.path.join(task_data_dir, dataset, "tableB.csv"))
                info = self.load_json(
                    (os.path.join(task_data_dir, dataset, "info.json"))
                )

                train_gt = self.load_df(
                    os.path.join(os.path.join(task_data_dir, dataset, "train.csv"))
                )

                test_gt = self.load_df(
                    os.path.join(os.path.join(task_data_dir, dataset, f"{mode}.csv"))
                )

                cot_path = os.path.join(task_data_dir, dataset, f"cot.json")
                if os.path.exists(cot_path):
                    with open(cot_path, "r") as f:
                        cot_data = json.load(f)
                else:
                    cot_data = {}

                train_examples = self.load_em_examples(
                    left, right, train_gt, info, cot_data
                )
                test_examples = self.load_em_examples(
                    left, right, test_gt, info, cot_data
                )

                for i in range(len(test_examples)):
                    test_examples[i]["metadata"]["dataset"] = dataset
                    test_examples[i]["fewshot_candidates"] = train_examples

                datasets.extend(test_examples)

        if max_size is not None:
            datasets = self._random_sample(
                datasets, max_size, random_state=random_state
            )

        return datasets

    def load_em_examples(self, left, right, gt, info, cot_data):
        left = left.set_index("id")
        right = right.set_index("id")
        examples = []
        for _, row in gt.iterrows():
            row_l = left.loc[row.ltable_id]
            row_r = right.loc[row.rtable_id]
            label = row.label
            lrid = f"{row.ltable_id}-{row.rtable_id}"

            test_example = {
                "row_l": row_l,
                "row_r": row_r,
                "label": label,
                "metadata": {
                    "table": lrid,
                },
                "topic": info["topic"],
            }
            if lrid in cot_data:
                test_example["cot"] = cot_data[lrid]

            examples.append(test_example)
        return examples

    def augment_data(self, test_data_dict: dict, random_state: int) -> dict:
        data_dict_perturb = deepcopy(test_data_dict)
        row_l = data_dict_perturb["row_l"]
        row_r = data_dict_perturb["row_r"]
        row_l_perturb = row_l.sample(frac=1, random_state=random_state)
        row_r_perturb = row_r.sample(frac=1, random_state=random_state)
        data_dict_perturb["row_l"] = row_l_perturb
        data_dict_perturb["row_r"] = row_r_perturb
        return data_dict_perturb

    def shorten_data(self, test_data_dict: dict) -> dict:
        test_data_dict = deepcopy(test_data_dict)
        # try drop very long and na column
        row_l = test_data_dict["row_l"]
        row_r = test_data_dict["row_r"]

        # only drop na columns and very long column or unimportant columns
        row_l_nona = self.drop_long_na_column(row_l)
        row_r_nona = self.drop_long_na_column(row_r)
        test_data_dict["row_l"] = row_l_nona
        test_data_dict["row_r"] = row_r_nona
        return test_data_dict

    def drop_long_na_column(self, row):
        new_index = []
        for x in row.index:
            if (
                len(str(row[x])) <= 150
                and not pd.isna(row[x])
                and str(row[x]).lower() != "nan"
            ):
                new_index.append(x)
        return row[new_index]
