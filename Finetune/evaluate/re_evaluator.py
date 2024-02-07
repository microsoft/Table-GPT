from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator
import json

class REEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.group_keys = ["method", "benchmark", "seed"]
        self.merge_keys = ["method", "benchmark"]
        self.answer_key = "relationship"
        
    def _evaluate_row(self, y_true, y_pred):
        if y_pred in y_true:
            nTP = 1
        else:
            nTP = 0
            
        if str(y_true) == None:
            P = 0
        else:
            P = 1
        nFP = 1 - nTP
        nFN = P - nTP
        
        res = {
            "nTP": nTP,
            "nFP": nFP,
            "nFN": nFN,
        }
        return res
    
    def _compute_metric(self, res):
        tp = res["nTP"].values.sum()
        fp = res["nFP"].values.sum()
        fn = res["nFN"].values.sum()
        prec = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * prec * recall / (prec + recall)
        metric = {
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "prec": prec,
            "recall": recall,
            "f1": f1
        }
        return metric
        