import os
import pandas as pd
import utils
import numpy as np

version = "v4"

def get_train():
    data_path = f"VaryTrain{version}/VaryTrain-TrainData-FinalDatav4-tokens_4096-PerturbSample_0_2-Size_17909.jsonl"
    leave_out_tasks = ["EntityMatching", "SchemaMatching", "Row2RowFewshot", "DataImputation", "ErrorDetection"]
    data = pd.read_json(data_path, lines=True)
    data_tasks = [utils.parse_metadata(t)["task"] for t in data["metadata"].values]

    for task in leave_out_tasks:
        mask = [t!= task for t in data_tasks]
        assert(sum(mask) > 0)
        subset = data[mask]
        name = f"LeaveOneOut-TrainData-FinalData{version}-{task}-tokens_4096-Size_{len(subset)}.jsonl"
        save_path = utils.makedir(["LeaveOneOut"], name)
        utils.save_as_jsonl(subset, save_path)

def get_test():
    unwanted_benchmark = ["BuyRowByRowTest", "BuyTest", "RestaurantRowByRowTest", "RestaurantTest", "stanfordOriginal", "Wiki"]
    data_path = f"TrainTestDataFinalCombined{version}/TestData-FinalDatav4-tokens_4096-Size_78273.jsonl"
    leave_out_tasks = ["EntityMatching", "SchemaMatching", "Row2RowFewshot", "DataImputation", "ErrorDetection"]
    data = pd.read_json(data_path, lines=True)
    data_tasks = [utils.parse_metadata(t)["task"] for t in data["metadata"].values]
    for task in leave_out_tasks:
        mask = [t == task for t in data_tasks]
        assert(sum(mask) > 0)
        subset = data[mask]
        
        benchmark_mask = [utils.parse_metadata(b)["benchmark"] not in unwanted_benchmark for b in subset["metadata"]]
        subset = subset[benchmark_mask]
        
        name = f"LeaveOneOut-TestData-FinalData{version}-{task}-tokens_4096-Size_{len(subset)}.jsonl"
        save_path = utils.makedir(["LeaveOneOut"], name)
        utils.save_as_jsonl(subset, save_path)

get_train()
get_test()