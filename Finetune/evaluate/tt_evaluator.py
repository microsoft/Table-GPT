from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator
import json
import re

def extract_strings_within_curly_braces(text):
    pattern = r'{(.*?)}'  # Non-greedy regex pattern to match strings inside curly braces
    matches = re.findall(pattern, text)
    return matches

class TTEvaluator(BaseEvaluator):
    def __init__(self):
        self.group_keys = ["method", "benchmark", "seed"]
        self.merge_keys = ["method", "benchmark"]
        
    def _evaluate_row(self, y_true, y_pred):        
        correct = 1
        op_correct = 1
        if len(y_true) != len(y_pred):
            correct = 0
            op_correct = 0
        else:
            for y_t, y_p in zip(y_true, y_pred):
                for k, v in y_t.items():
                    if k not in y_p or y_p[k] != v:
                        correct = 0
                if "transformation" not in y_p:
                    op_correct = 0
                elif y_t["transformation"] != y_p["transformation"]:
                    op_correct = 0
        
        res = {
            "correct": correct,
            "op_correct": op_correct
        }
        return res
    
    def _get_gt(self, label):
        y_gt = json.loads(label)
        if type(y_gt) == dict:
            y_gt = [y_gt]
        return y_gt

    def _get_pred(self, completion):
        if completion.endswith(" END"):
            completion = completion[:-4]
        steps = extract_strings_within_curly_braces(completion)
        y_pred = []
        for step in steps:
            try:
                pred = json.loads("{" + step + "}")
            except:
                pred = {}
            y_pred.append(pred)
        return y_pred
    
    def _compute_metric(self, res):
        acc = res["correct"].values.mean()
        op_acc = res["op_correct"].values.mean()
        metric = {
            "acc": acc,
            "op_acc": op_acc
        }
        return metric
        