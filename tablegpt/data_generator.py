import pandas as pd
import numpy as np
from multiprocessing import Pool
from .prompt_generator import PromptGenerator
from .table_tasks.table_task_factory import TableTaskFactory
from typing import Optional, Union
from .table_tasks.base_table_task import BaseTableTask


class DataGenerator:
    def __init__(
        self,
        table_task: Union[str, BaseTableTask],
        mode: str = "train",
        num_test_fewshot_samples: int = 5,
        prob_train_fewshot: float = 0.5,
        max_num_train_fewshot_samples: int = 10,
        min_num_train_fewshot_samples: int = 1,
        max_size: Optional[int] = None,
        max_token_length: int = 4096,
        drop_long_prompt: bool = True,
        random_state: int = 1,
        verbose: bool = False,
        use_random_template: bool = False,
        use_cot: bool = False,
        n_jobs: int = 1,
        augment: bool = False,
    ):
        if type(table_task) == str:
            self.table_task = TableTaskFactory.get_table_task(table_task)
        else:
            self.table_task = table_task

        self.mode = mode
        self.max_token_length = max_token_length
        self.num_test_fewshot_samples = num_test_fewshot_samples
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.prob_train_fewshot = prob_train_fewshot
        self.max_num_train_fewshot_samples = max_num_train_fewshot_samples
        self.min_num_train_fewshot_samples = min_num_train_fewshot_samples
        self.verbose = verbose
        self.max_size = max_size
        self.use_random_template = use_random_template
        self.use_cot = use_cot
        self.drop_long_prompt = drop_long_prompt
        self.augment = augment

    def generate_data(
        self, test_data_dir: str, train_data_dir: Optional[str] = None
    ) -> pd.DataFrame:
        # load train datasets
        self.print_log("Loading training and test data.")

        train_datasets = self.table_task.load_datasets(
            train_data_dir,
            n_jobs=self.n_jobs,
            random_state=self.random_state,
        )
        test_datasets = self.table_task.load_datasets(
            test_data_dir,
            n_jobs=self.n_jobs,
            max_size=self.max_size,
        )

        # generate test_data
        self.print_log("Generating prompt and completion.")
        test_data = self._generate_data(test_datasets, train_datasets)

        # remove invalid data for training
        if self.mode == "train" and len(test_data) > 0:
            na_mask = test_data["prompt"].isna()
            test_data = test_data[~na_mask]

        self.print_log("Size of data generated:", len(test_data))
        return test_data

    def _generate_data(self, test_datasets, train_datasets):
        all_args = []

        for idx, test_example in enumerate(test_datasets):
            # use train datasets as fewshot candidates if they are not provided
            if "fewshot_candidates" not in test_example:
                test_example["fewshot_candidates"] = train_datasets

            # set seed and num fewshot samples
            if self.mode == "train":
                # set seed with dataset index (different seed for different test examples in training mode)
                seed = self.random_state + idx
                # get numbers of few shot
                num_fewshot_samples = self._get_random_mixed_shot_num(random_state=seed)
            else:
                # set seed with dataset index (same seed for different test examples in test mode)
                seed = self.random_state
                num_fewshot_samples = self.num_test_fewshot_samples

            all_args.append([test_example, num_fewshot_samples, seed])

        # generate data for each example in parallel with multiprocessing
        if self.n_jobs == 1:
            results = [self.generate_data_one_example(*args) for args in all_args]
        else:
            with Pool(self.n_jobs) as pool:
                results = pool.starmap(self.generate_data_one_example, all_args)

        # merge all generated data and remove invalid ones
        if len(results) > 0:
            data_df = pd.concat(results, axis=0).reset_index(drop=True)
            return data_df
        else:
            return []

    def generate_data_one_example(self, test_example, num_fewshot_samples, seed=1):
        # retrieve fewshot examples
        fewshot_candidates = test_example.get("fewshot_candidates", [])
        if fewshot_candidates is not None and len(fewshot_candidates) > 0:
            fewshot_examples = self._random_sample(
                fewshot_candidates, num_fewshot_samples, random_state=seed
            )
        else:
            fewshot_examples = []

        if self.augment:
            test_example = self.table_task.augment_data(test_example, random_state=seed)
            fewshot_candidates_augment = [
                self.table_task.augment_data(example, random_state=seed)
                for example in fewshot_candidates
            ]
            fewshot_candidates = fewshot_candidates_augment

        # initalize prompt generator
        prompt_generator = PromptGenerator(
            table_task=self.table_task,
            max_token_length=self.max_token_length,
            drop_long_prompt=self.drop_long_prompt,
            use_random_template=self.use_random_template,
            use_cot=self.use_cot,
            random_state=seed,
        )

        # geenrate prompt and completion
        prompt = prompt_generator.generate_prompt(test_example, fewshot_examples)
        completion = prompt_generator.generate_completion(test_example)

        # save data and metadata into a dataframe
        data = {
            "prompt": prompt,
            "completion": completion,
        }
        metadata = {
            "task": self.table_task.__class__.__name__,
            "num_fewshots": len(fewshot_examples),
            "seed": seed,
        }
        if self.augment:
            metadata["augmentation_seed"] = seed

        if "metadata" in test_example:
            metadata.update(test_example["metadata"])

        data["metadata"] = metadata
        data_df = pd.DataFrame([data])
        return data_df

    def _get_random_mixed_shot_num(self, random_state):
        np.random.seed(random_state)
        if np.random.rand() < self.prob_train_fewshot:
            num_samples = np.random.randint(
                self.min_num_train_fewshot_samples,
                self.max_num_train_fewshot_samples + 1,
            )
        else:
            num_samples = 0
        return num_samples

    def _random_sample(self, data, n_samples, random_state):
        num = min(len(data), n_samples)
        np.random.seed(random_state)
        indices = np.random.choice(len(data), num, replace=False)
        samples = [data[i] for i in indices]
        return samples

    def print_log(self, *args):
        if self.verbose:
            print(*args)
