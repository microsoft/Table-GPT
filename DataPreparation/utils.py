import os
import pandas as pd
import numpy as np
from collections import defaultdict

def makedir(dir_list, file=None, replace=False):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def train_test_split(files, n_test, seed=1):
    np.random.seed(seed)
    files_shuffled = np.random.permutation(files)
    test_files = files_shuffled[:n_test]
    train_files = files_shuffled[n_test:]
    return test_files, train_files

def random_sample(files, n_test, seed=1):
    np.random.seed(seed)
    files_shuffled = np.random.permutation(files)
    sample = files_shuffled[-n_test:]
    return sample

def train_test_split_synthetic(files, n_test, seed=1):
    # group by file base
    groups = defaultdict(list)
    
    for f in files:
        base = f.split("_____")[0]
        groups[base].append(f)
    
    np.random.seed(seed)
    bases = sorted(groups.keys())
    bases_shuffled = np.random.permutation(bases)
    
    test_files = []
    train_files = []
    for base in bases_shuffled:
        if len(test_files) < n_test:
            test_files.extend(groups[base])
        else:
            train_files.extend(groups[base])
         
    return test_files, train_files

def load_api_keys(path):
    api_keys = []
    with open(path, "r") as f:
        for l in f:
            api_keys.append(l.strip())
    return api_keys

def get_model_name(model):
    if model == "D3":
        model_name = "text-davinci-003"
    elif model == "T3.5":
        model_name = "gpt-3.5-turbo"
    elif model == "A":
        model_name = "text-ada-001"
    elif model == "B":
        model_name = "text-babbage-001"
    elif model == "C":
        model_name = "text-curie-001"
    else:
        raise Exception(f"Wrong GPT model name: {model}")
    return model_name


def is_good_text_column(values):
    def check_column_length(values):
        length = [len(str(v)) for v in values if not isna(v)]
        if len(length) == 0:
            return False
        
        if max(length) > 30:
            return False
        
        if min(length) < 3:
            return False
        
        return True

    def check_na(values):
        for v in values:
            if isna(v):
                return False
        return True

    def check_num(values):
        for v in values:
            if has_num(v):
                return False
        return True

    def check_text(values):
        for v in values:
            if not has_text(v):
                return False
        return True

    def isna(v):
        return pd.isna(v) or str(v).lower() == "nan"
        
    def has_text(x):
        return any(char.isalpha() for char in str(x))

    def has_num(x):
        return any(char.isnumeric() for char in str(x))
    
    return check_column_length(values) and check_na(values) and check_num(values) and check_text(values)

def load_version(data_dir):
    with open(os.path.join(data_dir, "version"), "r") as f:
        line = f.readlines()
    return line[0].strip()

def save_version(data_dir, version):
    with open(os.path.join(data_dir, "version"), "w") as f:
        f.write(version)