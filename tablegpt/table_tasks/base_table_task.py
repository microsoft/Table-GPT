import os
import json
import pandas as pd
from typing import List
import numpy as np
from multiprocessing import Pool


class BaseTableTask:
    def __init__(self):
        pass

    def get_task_descriptions(self, test_example: dict) -> List[str]:
        # Return the task descriptions. Multiple descriptions can be returned in a list for prompt variation.
        raise Exception("Not implemented")

    def get_input(self, test_example: dict) -> str:
        # Define the prompt for input
        raise Exception("Not implemented")

    def get_output(self, test_example: dict) -> str:
        # Define the prompt for output
        raise Exception("Not implemented")

    def get_output_template(self, test_example: dict) -> str:
        # Define the template for output format
        raise Exception("Not implemented")

    def augment_data(self, test_data_dict: dict, random_state: int) -> dict:
        # Define how the data can be augmented (e.g., column permutation) if possible
        print("Warning: data augmentation is not implemented. Use original data.")
        return test_data_dict

    def shorten_data(self, test_data_dict: dict) -> dict:
        # If the prompt is too long, this function will be called to truncate data
        return test_data_dict

    def get_cot_output(self, test_example):
        answer = self.get_output(test_example)
        cot = test_example.get("cot", None)
        if cot is not None:
            completion = f"{cot.strip()} Therefore, the final answer is: \n{answer}"
        else:
            completion = answer
        return completion

    def load_data_example(self, data_dir: str) -> dict:
        info = self.load_json(os.path.join(data_dir, "info.json"))
        df = self.load_df(os.path.join(data_dir, "input_table.csv"))
        example = {"input_table": df}
        example.update(info)
        return example

    def load_test_example(self, data_dir: str) -> dict:
        test_example = self.load_data_example(data_dir)
        table_name = data_dir.split("/")[-1]
        dataset_name = data_dir.split("/")[-2]
        test_example["metadata"] = {"dataset": dataset_name, "table": table_name}

        if os.path.exists(os.path.join(data_dir, "fewshot_candidates")):
            fewshot_candidates = []
            for sample in os.listdir(os.path.join(data_dir, "fewshot_candidates")):
                fewshot_sample = self.load_data_example(
                    os.path.join(data_dir, "fewshot_candidates", sample)
                )
                fewshot_candidates.append(fewshot_sample)

            if len(fewshot_candidates) > 0:
                test_example["fewshot_candidates"] = fewshot_candidates

        return test_example

    def load_datasets(self, task_data_dir, n_jobs=1, max_size=None, random_state=1):
        example_paths = []

        if os.path.exists(task_data_dir):
            for dataset in sorted(os.listdir(task_data_dir)):
                for table in sorted(os.listdir(os.path.join(task_data_dir, dataset))):
                    example_paths.append(os.path.join(task_data_dir, dataset, table))

        if max_size is not None:
            example_paths = self._random_sample(
                example_paths, max_size, random_state=random_state
            )

        if n_jobs == 1:
            datasets = [self.load_test_example(path) for path in example_paths]
        else:
            with Pool(n_jobs) as pool:
                datasets = pool.map(self.load_test_example, example_paths)
        return datasets

    def load_df(self, df_path: str) -> pd.DataFrame:
        try:
            df = pd.read_csv(df_path, dtype=str)
        except:
            try:
                df = pd.read_csv(df_path, encoding="latin", dtype=str)
            except Exception as e:
                print(str(e))
                raise
        return df

    def load_json(self, json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        return data

    def answer_to_json(self, key, value):
        return json.dumps({key: value})

    def serialize_df(self, df):
        text = [""]
        for c in df.columns:
            text.append(str(c))
        text.append("\n")

        # add separating line
        for c in df.columns:
            text.append("---")
        text.append("\n")

        for row in df.values:
            for x in row:
                text.append(str(x))
            text.append("\n")
        return "|".join(text)

    def serialize_row(self, row):
        df = row.to_frame().T
        return self.serialize_df(df)

    def _random_sample(self, data, n_samples, random_state):
        num = min(len(data), n_samples)
        np.random.seed(random_state)
        indices = np.random.choice(len(data), num, replace=False)
        samples = [data[i] for i in indices]
        return samples
