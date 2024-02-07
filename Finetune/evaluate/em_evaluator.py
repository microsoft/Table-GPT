from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from collections import defaultdict
import numpy as np
import pandas as pd
import utils
import os
from .base_evaluator import BaseEvaluator

class EMEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.answer_key = "answer"
        
    def _compute_metric(self, res):
        y_true = res["y_gt"].apply(lambda x: int(x.lower() == "yes"))
        y_pred = res["y_pred"].apply(lambda x: int(x.lower() == "yes"))

        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred)
        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        metrics = {
            "prec": prec,
            "recall": rec,
            "acc": acc,
            "f1": f1
        }
        return metrics

    def save_debug(self, result, debug_dir):
        for (benchmark, dataset, seed, method), group_df in result.groupby(["benchmark", "dataset", "seed", "method"]):
            group_df.to_csv(utils.makedir([debug_dir], f"{benchmark}_{dataset}_{method}_{seed}.csv"), index=False)

    def _evaluate_row(self, y_true, y_pred):
        res = {
            "correct": int(y_true.lower() == y_pred.lower())  
        }
        return res
