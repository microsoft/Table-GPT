from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator
import json

class TQEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.answer_key = "answer"
        
    def _evaluate_row(self, y_true, y_pred):
        if str(y_true).lower() == str(y_pred).lower():
            correct = 1
        else:
            correct = 0
        res = {
            "correct": correct
        }
        return res
    
    def _compute_metric(self, res):
        acc = res["correct"].values.mean()
        metric = {
            "acc": acc
        }
        return metric
        