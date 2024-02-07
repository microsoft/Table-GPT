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

result_dir = "main_results"
method_alias = {
    "GPT-3.5": ["Result_vanilla"],
    "TableGPT": ["Result-VaryTrain-ModelD-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-FinalDatav2-UnseenAndSeenExcludeEM-Size_26489",
                 "Result-VaryTrain-ModelD-002___TrainData-FinalDatav4-PerturbSample_0_2-Size_17909___TestData-FinalDatav2-EM-only-Size_51784"]
}

def plot_bar(df, save_path):
    grouped = df.groupby(["method", "benchmark"])
    method_1 = "GPT-3.5"
    method_2 = "TableGPT"

    # Calculate the mean performance for each group
    means = grouped.mean().reset_index()
    means = means.sort_values(by="method", ascending=False)

    # Width of a bar
    width = 0.35
    
    num_benchmarks = df.shape[0]
    fig_width = max(num_benchmarks * width * 5, 6)

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(fig_width, 6))
    ax.set_xlim(-1, num_benchmarks)

    # X-axis values for the bars
    x = range(len(means))

    # Plot Method1 bars
    bars1 = ax.bar(
        [i - width/2 for i in x],
        means[method_1],
        width,
        label=method_1,
    )

    # Plot Method2 bars
    bars2 = ax.bar(
        [i + width/2 for i in x],
        means[method_2],
        width,
        label=method_2,
    )

    # Set x-axis labels
    ax.set_xticks(x)
    ax.set_xticklabels([f"{benchmark}\n{setting}" for setting, benchmark in zip(means["method"], means["benchmark"])])

    # Add labels, title, and legend
    ax.set_ylabel("Performance")

    def add_numbers_on_top(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height:.2f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    add_numbers_on_top(bars1)
    add_numbers_on_top(bars2)

    # Show the plot
    # plt.tight_layout()
    plt.savefig(save_path)


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

def remove_unused_benchmark(df):
    df_merge = df.copy()
    unused_benchmark = ["RestaurantRowByRowTest", "BuyRowByRowTest", "BuyTest", "RestaurantTest", "stanfordOriginal"]
    mask = [x not in unused_benchmark for x in df["benchmark"].values]
    return df_merge[mask]

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

def rename_task(df):
    df = df.copy()
    # rename missing cell
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
    old_task = df["task"].values
    new_task = []
    for t in old_task:
        new_task.append(col_rename[t])
    
    df["task"] = new_task
    return df

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

def rename_benchmark(df):
    df = df.copy()
    new_bench = []
    for _, row in df.iterrows():
        if row.task == "MissingCellColNoSep":
            new_bench.append("ExcelSyntheticColNoSep")
        elif row.task == "MissingCellColSep":
            new_bench.append("ExcelSyntheticColSep")
        elif row.task == "MissingCellRowNoSep":
            new_bench.append("ExcelSyntheticRowNoSep")
        elif row.task == "MissingCellRowSep":
            new_bench.append("ExcelSyntheticRowSep")
        else:
            new_bench.append(row.benchmark)
    df["benchmark"] = new_bench
    return df

def stack_method(df):
    groups = []
    for m, sub in df.groupby(["method"]):
        sub = sub.set_index(["task_type", "task"]).drop(columns="method")
        column_map = {c:c + " " + m for c in sub.columns.tolist()}
        sub = sub.rename(columns=column_map)
        groups.append(sub)
    stack = pd.concat(groups[::-1], axis=1)
    columns = ["GPT-3.5 Zero-Shot", "GPT-3.5 Few-Shot", "TableGPT Zero-Shot", "TableGPT Few-Shot"]
    stack = stack[columns].reset_index()
    return stack

def compute_avg(df):
    avg_df = df.groupby(by=["task_type", "method", "task"]).mean().reset_index()
    avg_df = avg_df.sort_values(by=["task_type", "method", "task"], ascending=False)
    return avg_df
    
result_df = pd.read_csv(os.path.join(result_dir, "csv", "overall_average.csv"))
result_df = merge_df(result_df)
result_df = rename_method(result_df)
result_df = remove_unused_benchmark(result_df)
result_df = add_type(result_df)
result_df = rename_benchmark(result_df)
result_df = rename_task(result_df)
result_df.to_excel(makedir(["report_data", "result_002"], "main_result.xlsx"), index=False)

avg_df = compute_avg(result_df)
avg_df.to_excel(makedir(["report_data", "result_002"], "main_result_avg.xlsx"), index=False)

avg_stack_df = stack_method(avg_df)
avg_stack_df.to_excel(makedir(["report_data", "result_002"], "main_result_avg_stack.xlsx"), index=False)
# print(result_df)
# for task, sub_result in result_df.groupby(by="task"):
#     save_path = makedir(["performance"], f"{task}.png")
    
