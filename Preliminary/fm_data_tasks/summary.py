import json
import os
import sys
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
def listdir(d):
    return [f for f in os.listdir(d) if "." not in f]

result_dir = sys.argv[1]

def compute_metrics(results):
    metrics = {"prec":[], "rec": [], "f1": [], "acc": []}
    for res in results:
        preds = res["preds_int"].values
        gts = res["label_int"].values
        correct = res["correct"]
        prec = precision_score(gts, preds)
        recall = recall_score(gts, preds)
        f1 = f1_score(gts, preds)
        acc = correct.mean()
        metrics["prec"].append(prec)
        metrics["rec"].append(recall)
        metrics["acc"].append(acc)
        metrics["f1"].append(f1)
    
    for k in ["prec", "rec", "f1", "acc"]:
        metrics["avg_" + k] = np.array(metrics[k]).mean()
        metrics["std_" + k] = np.array(metrics[k]).std()
    return metrics
    
summary = []
for d in listdir(result_dir):
    summ = {"dataset": d}
    # with open(os.path.join(result_dir, d, "metrics.json"), "r") as f:
    #     metric = json.load(f)
    results = []
    for trial in listdir(os.path.join(result_dir, d)): 
        if not os.path.exists(os.path.join(result_dir, d, trial, "result.csv")):
            continue
        res = pd.read_csv(os.path.join(result_dir, d, trial, "result.csv"))
        results.append(res)
    metric = compute_metrics(results)
    
    for k, v in metric.items():
        if type(v) == list:
            summ[k] = ",".join(["{:.3f}".format(x) for x in v])
        else:
            summ[k] = "{:.3f}".format(v)
    
    summ["avg_f1_std"] = "{}+/-{}".format(summ["avg_f1"], summ["std_f1"])
            
    summary.append(summ)
summary = pd.DataFrame(summary).sort_values(by="dataset", key=lambda col: col.str.lower())
summary.to_csv(os.path.join(result_dir, "summary.csv"), index=False)
