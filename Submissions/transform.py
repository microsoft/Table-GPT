import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt
def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir


def remove_unused_benchmark(data):
    unwanted_benchmark = ["BuyRowByRowTest", "BuyTest", "RestaurantRowByRowTest", "RestaurantTest", "stanfordOriginal", "Wiki"]
    benchmarks = [parse_metadata(x)["benchmark"] for x in data["metadata"].values]
    tasks =  [parse_metadata(x)["task"] for x in data["metadata"].values]
    mask = [b not in unwanted_benchmark for b in benchmarks]
    data = data[mask]
    
    # remove ExcelSynthetic for ED
    benchmarks = [parse_metadata(x)["benchmark"] for x in data["metadata"].values]
    tasks =  [parse_metadata(x)["task"] for x in data["metadata"].values]
    mask = [not (t == "ErrorDetection" and b == "ExcelSynthetic") for t, b in zip(tasks, benchmarks)]
    data = data[mask]
    return data

def save_as_jsonl(df, jsonl_save_dir):
    return df.to_json(jsonl_save_dir, orient='records', lines=True)

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def parse_metadata(metadata):
    key_value_list = metadata.split("___")
    result = {}
    for key_value in key_value_list:
        key = key_value.split("_")[0]
        value = key_value[len(key)+1:]
        result[key] = value
    return result

result_dir = "main_results"
method_alias = {
    "GPT-3.5": ["Result_vanilla",
                "Result-Vanilla-ModelD-002-FinalData___TestData-NewCF-CF-Size_1682",
                "Result-Vanilla-ModelD-002-FinalData___TestData-AddFewShot-data_v11_18_27-tokens_4096-CF-TQ-Size10370"],
    "Table-GPT-3.5": ["Result-VaryTrain-ModelD-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-FinalDatav2-UnseenAndSeenExcludeEM-Size_26489",
                      "Result-VaryTrain-ModelD-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-FinalDatav2-EM-only-Size_51784",
                      "Result-VaryTrain-ModelD-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-NewCF-CF-Size_1682",
                      "Result-VaryTrain-ModelD-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-AddFewShot-data_v11_18_27-tokens_4096-CF-TQ-Size10370"],
    "ChatGPT": ["Result-SecondBaseModel-Vanilla-ModelD-chat-002-FinalData___Test-UnseenAndSeenExcludeEM-Size_26489",
                "Result-Vanilla-ModelD-chat-002-FinalData___TestData-NewCF-CF-Size_1682",
                "Result-Vanilla-ModelD-Chat-002-FinalData___TestData-AddFewShot-data_v11_18_27-tokens_4096-CF-TQ-Size10370",
                ],
    "Table-ChatGPT": ["Result-SecondBaseModel-ModelD-chat-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-All-Size_78273",
                      "Result-VaryTrain-ModelD-Chat-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-NewCF-CF-Size_1682",
                      "Result-VaryTrain-ModelD-Chat-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-AddFewShot-data_v11_18_27-tokens_4096-CF-TQ-Size10370"
                      ]
}

def merge_values(arr):
    result = []
    count_multiple_non_nan = 0

    for row in arr:
        non_nan_values = [x for x in row if not np.isnan(x)]
        if non_nan_values:
            result.append(non_nan_values[0])
            if len(non_nan_values) > 1:
                count_multiple_non_nan += 1
        else:
            result.append(np.nan)

    return np.array(result), count_multiple_non_nan

def rename_method(df):
    df_merge = df.copy()
    new_method = []
    for _, row in df.iterrows():
        if row["task"] == "Row2RowFewshot":
            new_method.append("Few-Shot")
            continue
        
        x = row["method"]
        if x == "random0":
            new_method.append("Zero-Shot")
        elif "stanford" in x:
            new_method.append("Manual Few-Shot")
        else:
            new_method.append("Few-Shot")
    df_merge["method"] = new_method
    return df_merge

def merge_df(df):
    df_merge = df.copy()
    for name, file_list in method_alias.items():
        res = df_merge[file_list].values
        merge_res, count_conflict= merge_values(res)
        if count_conflict > 0:
            print("Warning conflict of results in", name)
        df_merge[name] = merge_res
        df_merge = df_merge.drop(columns=file_list)
    return df_merge

def rename_task(task):
    col_rename = {
        "ColumnFinding": "Column Finding",
        "MissingCellColNoSep": "Missing Value Identification", 
        "MissingCellColSep": "Missing Value Identification",
        "MissingCellRowNoSep": "Missing Value Identification",
        "MissingCellRowSep": "Missing Value Identification",
        "Row2RowFewshot": "Row-to-Row Transformation",
        "ColumnTypeAnnotation": "Column Type Annotation",
        "DataImputation": "Data Imputation",
        "ErrorDetection": "Error Detection",
        "EntityMatching": "Entity Matching",
        "SchemaMatching": "Schema Matching",
        "TableQuestion": "Table Question"
    }
    if task in col_rename:
        return col_rename[task]
    return task

def add_type(df):
    col_rename = {
        "ColumnFinding": "Unseen",
        "MissingCellColNoSep": "Unseen", 
        "MissingCellColSep": "Unseen",
        "MissingCellRowNoSep": "Unseen",
        "MissingCellRowSep": "Unseen",
        "Row2RowFewshot": "Unseen",
        "ColumnTypeAnnotation": "Unseen",
        "DataImputation": "Seen",
        "ErrorDetection": "Seen",
        "EntityMatching": "Seen",
        "SchemaMatching": "Seen",
        "TableQuestion": "Seen"
    }
    old_task = df["task"].values
    new_task = []
    for t in old_task:
        new_task.append(col_rename[t])
    
    df["task_type"] = new_task
    return df

def rename_benchmark(meta):
    if meta["task"] == "MissingCellColNoSep":
        return "Column (no seperator)"

    if meta["task"]== "MissingCellColSep":
        return "Column (with seperator)"
    
    if meta["task"]== "MissingCellRowNoSep":
        return "Row (no seperator)"
    
    if meta["task"]== "MissingCellRowSep":
        return "Row (with seperator)"

    if meta["task"] == "ColumnFinding" and meta["benchmark"] == "ExcelSynthetic":
        return "Spreadsheets-CF"

    if meta["task"] == "ColumnTypeAnnotation":
        if meta["benchmark"] == "EfthymiouTest":
            return "Efthymiou"
        elif meta["benchmark"] == "T2DTest":
            return "T2D"
        elif meta["benchmark"] == "SherlockTest":
            return "Sherlock"
        elif meta["benchmark"] == "LimayeTest":
            return "Limaye"
        else:
            raise
    
    if meta["task"] == "TableQuestion" and meta["benchmark"] == "WikiTest":
        return "WikiTest"

    if meta["task"] == "EntityMatching":
        return meta["dataset"]

    if meta["task"] == "ErrorDetection":
        if meta["benchmark"] == "ExcelRealV6":
            return "Spreadsheets-Real"
        elif meta["benchmark"] == "WebRealV6":
            return "WebTables-Real"
        else:
            print(meta["benchmark"])
            raise
    
    if meta["task"] == "Row2RowFewshot":
        if "benchmark-stackoverflow" in meta["filename"]:
            return "Stackoverflow"
        elif "unit" in meta["filename"]:
            return "BingQL-Unit"
        elif "benchmark-FF-Trifacta-GoogleRefine" in meta["filename"]:
            return "FF-GR-Trifacta"
        elif "benchmark-headcase" in meta["filename"]:
            return "Headcase"
        else:
            return "BingQL-other"

    if meta["benchmark"] == "WikiTest":
        return "Wiki"
        
    return meta["benchmark"]

def remove_ending(completion):
    while True:
        if completion.endswith(" END"):
            completion = completion[:-4]
        else:
            break
    return completion.strip()

for name, files in method_alias.items():
    result = []
    for f in files:
        print(f)
        res = pd.read_json(os.path.join("main_results", "preds", f+".jsonl"), lines=True)
        result.append(res)
    result = pd.concat(result, axis=0).reset_index(drop=True)
    result = remove_unused_benchmark(result)

    # parse meta
    new_result = []
    for _, row in result.iterrows():
        meta = parse_metadata(row["metadata"])
        
        setting = "Zero-Shot" if meta["numSamples"] == "0" else "Few-Shot"
        if meta["task"] == "Row2RowFewshot":
            setting = "Few-Shot"
        benchmark = rename_benchmark(meta)
        task = rename_task(meta["task"])
        if meta["task"] == "EntityMatching":
            case = meta["lrid"]
        else:
            case = meta["dataset"]
        
        new_row = {
            "task": task,
            "dataset": benchmark,
            "case": case,
            "setting": setting,
            "prompt": row["prompt"],
            "completion": remove_ending(row.choices[0]["text"]),
            "label": remove_ending(meta["completion"]),
        }
        new_result.append(new_row)
    
    new_result = pd.DataFrame(new_result)
    jsonl_save_dir = f"result_{name}.jsonl"
    save_as_jsonl(new_result, makedir(["results"], jsonl_save_dir))
    