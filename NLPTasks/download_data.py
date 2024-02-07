from datasets import load_dataset
import os
import json
import numpy as np

root_save_dir = "../Finetune/data/data_vglue"

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def save_data(dataset, save_dir, mode, max_num=2000):
    np.random.seed(1)
    if len(dataset) <= max_num:
        indices = np.arange(max_num)
    else:
        indices = np.random.permutation(len(dataset))[:max_num]
    
    indices = set(indices)
    
    for i, data in enumerate(dataset):
        if i in indices:
            with open(makedir([save_dir, f"{mode}{i}"], "info.json"), "w") as f:
                json.dump(data, f)

template_dir = "template"
tasks = ["ax", "cola", "mnli_matched", "mnli_mismatched", "mrpc", "qnli", "qqp", "rte", "sst2", "wnli", "stsb"]

for task in tasks:
    # load data
    if "mnli" in task:
        train_data = load_dataset('glue', "mnli", split='train')
    else:
        train_data = load_dataset('glue', task, split='train')
    
    save_data(train_data, makedir([root_save_dir, task, "train", "glue"]), "train")
  
    # check test label exists or not
    test_data = load_dataset('glue', task, split='validation')
    labels = set([row["label"] for row in test_data])
    
    if len(labels) == 1:
        raise
        # print(task, labels)
        # test_data = load_dataset('glue', task, split='validation') # cola test not public    

    test_data.to_csv(makedir(["check"], f"{task}.csv"), index=False)
    save_data(test_data, makedir([root_save_dir, task, "test", "glue"]), "test")
