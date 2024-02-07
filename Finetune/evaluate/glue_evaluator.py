from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, matthews_corrcoef
import utils
import os
from .base_evaluator import BaseEvaluator
import json

class GlueEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.answer_key = "answer"
        self.group_keys = ["method", "benchmark", "seed"]
        self.merge_keys = ["method", "benchmark"]

    def ans_to_int(self, ans):
        if self.task_name in ["cola", "mrpc", "qnli", "qqp", "rte", "wnli"]:
            return int(str(ans).lower() == "yes")
        elif self.task_name == "sst2":
            return int(str(ans).lower() == "positive")
        else:
            if self.task_name == "mnli":
                if str(a).lower() == "entialment":
                    return 1
                elif str(a).lower() == "contradiction":
                    return 2
                else:
                    return 0
        
    def _evaluate_row(self, y_true, y_pred):
        if str(y_true).lower() == str(y_pred).lower():
            correct = 1
        else:
            correct = 0
        
        y_true_int = self.ans_to_int(y_true)
        y_pred_int = self.ans_to_int(y_pred)
        
        res = {
            "correct": correct,
            "y_true_int": y_true_int,
            "y_pred_int": y_pred_int
        }
        return res
    
    def _compute_metric(self, res):
        acc = res["correct"].values.mean()
        metric = {
            "acc": acc,
        }
        if self.task_name == "cola":
            metric["matthews_corr"] = matthews_corrcoef(res["y_true_int"].values, res["y_pred_int"].values)
            
        return metric
        