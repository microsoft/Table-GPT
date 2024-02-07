from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator

class TMEvaluator(BaseEvaluator):
    def _evaluate_row(self, y_true, y_pred):
        if y_true.strip().lower() == y_pred.strip().lower():
            correct = 1
        else:
            correct = 0
            
        res = {
            "correct": correct
        }
        return res
    
    def _get_gt(self, label):
        return label

    def _get_pred(self, completion):
        if completion.endswith(" END"):
            completion = completion[:-4]
        return completion
    
    def _compute_metric(self, res):
        acc = res["correct"].values.mean()
        metric = {
            "acc": acc
        }
        return metric
        