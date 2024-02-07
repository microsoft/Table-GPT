import pandas as pd
import os
from shutil import copytree

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

test_tasks = ["ColumnTypeAnnotation","EntityMatching","MissingCell","TableQuestion","DataImputation","ErrorDetection","SchemaMatching", "ColumnFinding", "Row2Row"]
unwanted_benchmark = ["BuyRowByRowTest", "BuyTest", "RestaurantRowByRowTest", "RestaurantTest", "stanfordOriginal", "Wiki"]

alias = {
    "MissingCell": "MissingValueIdentification",
    "Row2Row": "RowToRowTransformation"
}

benchmark_alias = {
    "EfthymiouTest": "Efthymiou",
    "LimayeTest": "Limaye",
    "SherlockTest": "Sherlock",
    "T2DTest": "T2D",
    "ExcelRealV6": "Spreadsheets-Real",
    "WebRealV6": "WebTables-Real",
    "WikiTest": "Wiki"
}

data_dir = "data/data_v11.18"
save_dir = "TestData"

for t in test_tasks:
    test_data_dir = os.path.join(data_dir, t, "test")
    for benchmark in os.listdir(test_data_dir):
        if benchmark in unwanted_benchmark:
            continue
        
        if t in alias:
            task = alias[t]
        else:
            task = t
                        
        if t == "ErrorDetection" and benchmark == "ExcelSynthetic":
            continue

        if t == "DataImputation" and benchmark == "ExcelSynthetic":
            new_benchmark = "Spreadsheets-DI"        
        elif t == "MissingCell" and benchmark == "ExcelSynthetic":
            new_benchmark = "Spreadsheets-MVI"
        elif t == "ColumnFinding" and benchmark == "ExcelSynthetic":
            new_benchmark = "Spreadsheets-CF"
        elif benchmark in benchmark_alias:
            new_benchmark = benchmark_alias[benchmark]
        else:
            new_benchmark = benchmark
            
        if t == "EntityMatching":
            for d in os.listdir(os.path.join(test_data_dir, benchmark)):
                print(task, d)
                copytree(os.path.join(test_data_dir, benchmark, d), makedir([save_dir, task], d))
        elif t == "Row2Row":
            for filename in os.listdir(os.path.join(test_data_dir, benchmark)):
                if "benchmark-stackoverflow" in filename:
                    new_benchmark = "Stackoverflow"
                elif "unit" in filename:
                    new_benchmark = "BingQL-Unit"
                elif "benchmark-FF-Trifacta-GoogleRefine" in filename:
                    new_benchmark = "FF-GR-Trifacta"
                elif "benchmark-headcase" in filename:
                    new_benchmark = "Headcase"
                else:
                    new_benchmark = "BingQL-other"
                
                copytree(os.path.join(test_data_dir, benchmark, filename), makedir([save_dir, task, new_benchmark], filename))
            
        else:
            print(task, new_benchmark)
            copytree(os.path.join(test_data_dir, benchmark), makedir([save_dir, task], new_benchmark))
        