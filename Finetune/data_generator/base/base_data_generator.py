import os
import pandas as pd
import json
import numpy as np
from functools import partial
from multiprocessing import Pool
from copy import deepcopy
from tqdm import tqdm

class BaseDataGenerator(object):
    def __init__(self, 
                task,
                serializer,
                num_few_shot_trials=3, 
                num_few_shot_samples=10,
                num_col_perturb=30,
                prob_train_few_shot=0.5,
                max_train_num_few_shot_samples=10,
                min_train_num_few_shot_samples=4,
                max_train_size=500,
                max_token_length=2048,
                n_jobs=1,
                random_state=1,
                max_num_datasets=None,
                verbose=False,
                debug_dir=None,
                use_random_description=False,
                use_random_template=False,
                use_cot=False,
                cot_data_dir=None,
                cot_position="after_answer",
                use_system_message=False):
        self.task = task
        self.max_token_length = max_token_length
        self.num_few_shot_trials = num_few_shot_trials
        self.num_few_shot_samples = num_few_shot_samples
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.serializer = serializer
        self.debug_dir = debug_dir
        self.num_col_perturb = num_col_perturb
        self.prob_train_few_shot =prob_train_few_shot
        self.max_train_num_few_shot_samples = max_train_num_few_shot_samples
        self.min_train_num_few_shot_samples = min_train_num_few_shot_samples
        self.verbose = verbose
        self.max_train_size = max_train_size
        self.max_num_datasets = max_num_datasets
        self.use_random_description = use_random_description
        self.use_random_template = use_random_template
        self.use_cot = use_cot
        self.cot_data_dir = cot_data_dir
        self.cot_position = cot_position
        self.use_system_message = use_system_message
        
    def generate_data(self, data_dir, mode):
        self.mode = mode
        raw_train_datasets, raw_test_datasets = self._load_datasets(data_dir)
        self.raw_train_datasets = raw_train_datasets
        
        if mode == "train":
            datasets = raw_train_datasets
            func = partial(self.generate_train_one_dataset, datasets=datasets)
        else:
            datasets = raw_test_datasets
            func = partial(self.generate_test_one_dataset, datasets=datasets)
                    
        if self.max_num_datasets is None:
            indices = range(len(datasets))
        else:
            indices = self._random_sample(range(len(datasets)), self.max_num_datasets, random_state=self.random_state)

        if self.n_jobs == 1:
            results = []
            for i in tqdm(indices):
                results.append(func(i))
        else:
            with Pool(self.n_jobs) as pool:
                results = pool.map(func, indices)

        data_df = pd.concat(results, axis=0).reset_index(drop=True)
        na_mask = data_df["prompt"].isna()
        valid_df = data_df[~na_mask]
        invalid_df = data_df[na_mask]
        return valid_df, invalid_df
    
    def generate_train_one_dataset(self, idx, datasets):        
        test_dataset_info = deepcopy(datasets[idx])
        if self.verbose:
            print("Processing dataset", test_dataset_info["dataset"])
        
        # set seed with dataset index
        seed = self.random_state + idx
        
        # load test data
        test_data_dict = self._load_data_dict(test_dataset_info)
        
        # load fewshot data info
        fewshot_datasets_info = self._get_fewshot_datasets_info(test_dataset_info, "random")
        
        train_data = []
        # generate one mixed-shot train data
        num_samples = self._get_random_mixed_shot_num(random_state=seed)
        fewshot_data_dict = self._load_fewshot_data_dict(fewshot_datasets_info, num_samples=num_samples, random_state=seed)
        data_df = self._generate_data_one_case(test_data_dict, fewshot_data_dict, random_state=seed)
        train_data.append(data_df)
    
        # generate more train data with column perturb
        for i in range(self.num_col_perturb):
            perturb_test_data_dict = self._col_perturb_test_data(test_data_dict, random_state=seed+i)
            perturb_fewshot_data_dict = self._col_perturb_fewshot_data(fewshot_data_dict, random_state=seed+i)
            tag_dict = {"colPerturbSeed": seed+i}
            perturb_df = self._generate_data_one_case(perturb_test_data_dict, perturb_fewshot_data_dict, random_state=seed+i, tag_dict=tag_dict)    
            train_data.append(perturb_df)
            
        train_data = pd.concat(train_data, axis=0).reset_index(drop=True)

        if self.debug_dir is not None:
            save_path = os.path.join(self.debug_dir, f"{test_dataset_info['dataset']}.csv")
            train_data.to_csv(save_path, index=False)
        return train_data
    
    def generate_test_one_dataset(self, idx, datasets):
        test_dataset_info = deepcopy(datasets[idx])
        if self.verbose:
            print("Processing dataset", test_dataset_info["dataset"])
        
        seed = self.random_state
        
        # load test data
        test_data_dict = self._load_data_dict(test_dataset_info)
        
        # zero shot
        test_data = []
        zero_df = self._generate_data_one_case(test_data_dict, None, random_state=seed)
        test_data.append(zero_df)
        
        # load fewshot data info
        # few shot
        fewshot_datasets_info = self._get_fewshot_datasets_info(test_dataset_info, "random")
        if fewshot_datasets_info is not None:
            for trial_num in range(self.num_few_shot_trials):
                fewshot_data_dict = self._load_fewshot_data_dict(fewshot_datasets_info, num_samples=self.num_few_shot_samples, random_state=seed+trial_num)
                fewshot_df = self._generate_data_one_case(test_data_dict, fewshot_data_dict, random_state=seed+trial_num)
                test_data.append(fewshot_df)
            
        # stanford manual
        stanford_datasets_info = self._get_fewshot_datasets_info(test_dataset_info, "stanford")
        if stanford_datasets_info is not None:
            fewshot_data_dict = self._load_fewshot_data_dict(stanford_datasets_info, num_samples=self.num_few_shot_samples, random_state=seed)
            stanford_df = self._generate_data_one_case(test_data_dict, fewshot_data_dict, random_state=seed)
            test_data.append(stanford_df)
    
        test_data = pd.concat(test_data, axis=0).reset_index(drop=True)
        
        if self.debug_dir is not None:
            save_path = os.path.join(self.debug_dir, f"{test_dataset_info['benchmark']}_{test_dataset_info['dataset']}.csv")
            test_data.to_csv(save_path, index=False)
        return test_data
    
    def _generate_data_one_case(self, test_data_dict, fewshot_data_dict, random_state, tag_dict=None):
        """generate prompt and label with test data and fewshot data"""
        # initalize task descriptor
        task_descriptor_params = {
            "serializer": self.serializer, 
            "random_state": random_state, 
            "use_random_description": self.use_random_description,
            "use_cot": self.use_cot
        }
        task_descriptor_params.update(test_data_dict["task_descriptor_params"])
        task_descriptor = self._get_task_descriptor(task_descriptor_params)
        
        # initalize prompt generator
        prompt_generator_params = {
            "task_descriptor": task_descriptor,
            "max_token_length": self.max_token_length, 
            "min_fewshot_samples": self.min_train_num_few_shot_samples,
            "use_random_template": self.use_random_template,
            "random_state": random_state, 
            "use_system_message": self.use_system_message,
            "use_cot": self.use_cot
        }
        prompt_generator_params.update(test_data_dict["prompt_generator_params"])
        prompt_generator = self._get_prompt_generator(prompt_generator_params)
        
        test = test_data_dict["data"]
        label = test_data_dict["label"]
        
        if fewshot_data_dict is None:
            prompt = prompt_generator.generate_prompt(test, None)
        else:
            prompt = prompt_generator.generate_prompt(test, fewshot_data_dict["data_label_list"])
        
        completion = prompt_generator.generate_completion(label)
        sample_method = "random" if fewshot_data_dict is None else fewshot_data_dict["sample_method"]
        num_samples = 0 if fewshot_data_dict is None else fewshot_data_dict["num_samples"]
        
        data = {
            "task": self.task,
            "benchmark": test_data_dict["dataset_info"]["benchmark"],
            "dataset": test_data_dict["dataset_info"]["dataset"],
            "sampleMethod": sample_method,
            "numSamples": num_samples,
            "seed": random_state,
            "prompt": prompt,
            "completion": completion,
            "label": completion
        }
        data.update(test_data_dict["metadata"])
        data_df = pd.DataFrame([data])
        data_df["metadata"] = self._generate_metadata(data_df, tag_dict=tag_dict)
        return data_df
    
    def _get_random_mixed_shot_num(self, random_state):
        np.random.seed(random_state)
        if np.random.rand() < self.prob_train_few_shot:
            num_samples = np.random.randint(self.min_train_num_few_shot_samples, self.max_train_num_few_shot_samples+1)
        else:
            num_samples = 0
        return num_samples
    
    def _get_prompt_generator(self, params):
        raise Exception("Not implemented")
    
    def _get_task_descriptor(self, params):
        """Initialize task descriptor here."""
        raise Exception("Not implemented")

    def _col_perturb_test_data(self, test_data_dict, random_state) -> dict:
        raise Exception("Not implemented")

    def _col_perturb_fewshot_data(self, fewshot_data_dict, random_state) -> dict:
        raise Exception("Not implemented")

    def _load_data_label(self, data_info):
        data_dir = data_info["dataset_dir"]
        with open(os.path.join(data_dir, "info.json"), "r") as f:
            info = json.load(f)
        data = self.load_df(os.path.join(data_dir, "data.csv"))
        return data, info["label"]
    
    def _load_metadata(self, dataset_info):
        return {}
    
    def _load_prompt_generator_params(self, dataset_info):
        return {}
    
    def _load_task_descriptor_params(self, dataset_info):
        return {}

    def _load_data_dict(self, dataset_info) -> dict:
        data, label = self._load_data_label(dataset_info)
        metadata = self._load_metadata(dataset_info)
        prompt_generator_params = self._load_prompt_generator_params(dataset_info)
        task_descriptor_params = self._load_task_descriptor_params(dataset_info)
        
        data_dict = {
            "data": data,
            "label": label,
            "dataset_info": dataset_info,
            "metadata": metadata,
            "prompt_generator_params": prompt_generator_params,
            "task_descriptor_params": task_descriptor_params
        }
        return data_dict
    
    def _load_fewshot_data_dict(self, fewshot_datasets_info, num_samples, random_state):
        if fewshot_datasets_info is None:
            return None
        
        if num_samples == 0:
            fewshot_data_labels = None
        else:
            # take a sample and load data dict
            sample_datasets_info = self._random_sample(fewshot_datasets_info["datasets_info"], num_samples, random_state)
            fewshot_data_labels = []
            for dataset_info in sample_datasets_info:
                data, label = self._load_data_label(dataset_info)
                fewshot_data_labels.append((data, label))
                
        fewshot_data_dict = {
            "data_label_list": fewshot_data_labels,
            "sample_method": fewshot_datasets_info["sample_method"],
            "num_samples": num_samples,
            "random_state": random_state
        }
        return fewshot_data_dict
    
    def _get_fewshot_datasets_info(self, test_data_info, sample_method):
        if sample_method == "random":
            # sample fewshot from entire training datasets
            fewshot_datasets_info = {
                "datasets_info": self.raw_train_datasets,
                "sample_method": sample_method
            }
            return fewshot_datasets_info
        else:
            return None
        
    def _load_datasets(self, data_dir) -> list:
        """return a list of dictionary"""
        train_data_dir = os.path.join(data_dir, self.task, "train")
        test_data_dir = os.path.join(data_dir, self.task, "test")
        raw_train_datasets = self._get_datasets_info(train_data_dir)
        raw_test_datasets = self._get_datasets_info(test_data_dir)
        return raw_train_datasets, raw_test_datasets

    def _get_datasets_info(self, data_dir):
        datasets = []
        if not os.path.exists(data_dir):
            print("Not Exists Warning:", data_dir)
            return datasets
        for benchmark in sorted(os.listdir(data_dir)):
            for dataset in sorted(os.listdir(os.path.join(data_dir, benchmark))):
                dataset_info = {
                    "benchmark": benchmark,
                    "dataset": dataset,
                    "dataset_dir": os.path.join(data_dir, benchmark, dataset),
                }
                datasets.append(dataset_info)
        return datasets
    
    def _random_sample(self, data, n_samples, random_state):
        num = min(len(data), n_samples)
        np.random.seed(random_state)
        indices = np.random.choice(len(data), num, replace=False)
        samples = [data[i] for i in indices]
        return samples
    
    def _generate_metadata(self, test_df, tag_dict=None) -> str:
        """Return a dataframe containing prompt and completion"""
        metadata = []
        for _, row in test_df.iterrows():
            row_meta = []
            for k, v in row.items():
                if k != "prompt":
                    row_meta.append(f"{k}_{v}")
            if tag_dict is not None:
                for k, v in tag_dict.items():
                    row_meta.append(f"{k}_{v}")
            metadata.append("___".join(row_meta))
        return metadata

    def load_df(self, df_path, info=None):
        try:
            df = pd.read_csv(df_path, dtype=str)
        except:
            try:
                df = pd.read_csv(df_path, encoding="latin", dtype=str)
            except Exception as e:
                print(str(e))
                raise
        
        if info is not None:
            if "rename_columns" in info:
                df = df.rename(columns=info["rename_columns"])
            if "drop_columns" in info:
                drop_columns = [c for c in df.columns if c in info["drop_columns"]]
                df = df.drop(columns=drop_columns)
        return df

    def get_cot_data_path(self, dataset_path):
        suffix = "/".join(dataset_path.split("/")[3:])
        return os.path.join(self.cot_data_dir, self.task, suffix, "data.csv")