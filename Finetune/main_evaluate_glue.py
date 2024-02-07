import pandas as pd
import os
import argparse
import numpy as np
from datetime import date
import json
from sklearn.metrics import precision_score, recall_score, f1_score
from collections import defaultdict
import utils
import pickle
from evaluate.glue_evaluator import GlueEvaluator
import time

parser = argparse.ArgumentParser()
parser.add_argument("--result_dir", default=None)
parser.add_argument("--n_jobs", default=-1, type=int)
parser.add_argument("--debug", action="store_true", default=False)
args = parser.parse_args()

if args.n_jobs < 0:
    args.n_jobs = os.cpu_count()
    
summary_metric = {
    "cola":"acc",
    "mrpc":"acc",
    "qnli":"acc",
    "qqp":"acc",
    "rte":"acc",
    "wnli":"acc",
    "sst2":"acc",
    "mnli_mismatched":"acc",
    "mnli_matched":"acc", 
}

evaluator_dict = {
    "cola": GlueEvaluator(),
    "mrpc": GlueEvaluator(),
    "qnli": GlueEvaluator(),
    "qqp": GlueEvaluator(),
    "rte": GlueEvaluator(),
    "wnli": GlueEvaluator(),
    "sst2": GlueEvaluator(),
    "mnli_mismatched": GlueEvaluator(),
    "mnli_matched": GlueEvaluator(), 
}
    
summary_benchmarks = []
summary_tasks = defaultdict(list)

for jsonl_file in os.listdir(os.path.join(args.result_dir, "preds")):
    print("Evaluating", jsonl_file)
    model_name = jsonl_file[:-6]
    preds = pd.read_json(os.path.join(args.result_dir, "preds", jsonl_file), lines=True)
    preds["task"] = preds["metadata"].apply(lambda x: utils.parse_metadata(x)["task"])
    
    summary_benchmark_list = []
    for task, preds_group in preds.groupby("task"):
        # if task != "SemanticDedup":
        #     continue
        print(task)
        debug_dir = utils.makedir([args.result_dir, "debug", task, model_name]) if args.debug else None
        evaluator = evaluator_dict[task]
        evaluator.task_name = task
        avg_results, detail_results = evaluator.evaluate(preds_group, debug_dir=debug_dir, n_jobs=args.n_jobs)    
        avg_results.to_excel(utils.makedir([args.result_dir, "metrics", task], f"{model_name}_avg.xlsx"))
        detail_results.to_excel(utils.makedir([args.result_dir, "metrics", task], f"{model_name}_details.xlsx"))
        
        summ = avg_results[evaluator.merge_keys + [summary_metric[task]]].rename(columns={summary_metric[task]: f"{model_name}"})
        
        # average over benchmark
        summ_benchmark = summ.groupby(["method", "benchmark"], as_index=False).mean()
        summ_benchmark["task"] = task
        summary_benchmark_list.append(summ_benchmark)
        
        # save datasets results
        summ_task = summ.set_index(evaluator.merge_keys)
        summary_tasks[task].append(summ_task)
        
    summary_benchmark_df = pd.concat(summary_benchmark_list, axis=0)
    summary_benchmark_df = summary_benchmark_df.sort_values(by=["task", "method", "benchmark"]).set_index(["task", "method", "benchmark"])
    summary_benchmarks.append(summary_benchmark_df)

summary_benchmarks = pd.concat(summary_benchmarks, axis=1)
summary_benchmarks.to_excel(utils.makedir([args.result_dir, "summary"], f"overall_average.xlsx"))
summary_benchmarks.to_csv(utils.makedir([args.result_dir, "csv"], f"overall_average.csv"))

for task, summary in summary_tasks.items():
    res = pd.concat(summary, axis=1)
    res.to_excel(utils.makedir([args.result_dir, "summary"], f"{task}_summary.xlsx"))
    res.to_csv(utils.makedir([args.result_dir, "csv"], f"{task}_summary.csv"))

    