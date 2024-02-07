from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator
from multiprocessing import Pool
import json

class CTAEvaluator(BaseEvaluator):
    def __init__(self):
        self.group_keys = ["method", "benchmark", "seed"]
        self.merge_keys = ["method", "benchmark"]
        self.answer_key = "chosen_semantic_type"
        
    def _evaluate_row(self, y_true, y_pred):
        if str(y_true) == "None":
            y_true = []
            nP = 0
        else:
            nP = 1
        
        if str(y_pred) != "None" and y_pred == y_true:
            nTP = 1
        else:
            nTP = 0
            
        if str(y_pred) == "None":
            nPP = 0
        else:
            nPP = 1
            
        nFP = nPP - nTP
        nFN = nP - nTP
        
        res = {
            "nTP": nTP,
            "nFP": nFP,
            "nFN": nFN,
        }
        return res
    
    def _compute_metric(self, res):
        num_error = res["nFP"].values.sum()
        num_cands = res["numCandidates"].values.astype(int).sum()
        binary_acc = (num_cands - num_error) / num_cands
        
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
            "f1": f1,
            "binary_acc": binary_acc
        }
        return metric