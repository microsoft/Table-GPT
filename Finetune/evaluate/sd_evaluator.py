from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator
from multiprocessing import Pool
import json

class SDEvaluator(BaseEvaluator):
    def __init__(self):
        self.group_keys = ["method", "benchmark", "seed"]
        self.merge_keys = ["method", "benchmark"]
        self.answer_key = "inconsistent_pair"
        
    def _evaluate_row(self, y_true, y_pred):
        if str(y_true) == "None":
            nGT = 0
        else:
            nGT = 1
        
        if type(y_pred) == str and str(y_pred) == "None":
            nPred = 0
        else:
            nPred = 1
        
        nTP = 0
        if str(y_true) == "None" and str(y_pred) != "None" and set(y_true) == set(y_pred):
            nTP = 1
        
        nFP = nPred - nTP
        nFN = nGT - nTP

        res = {
            "nTP": nTP,
            "nFP": nFP,
            "nFN": nFN,
            "nGT": nGT,
            "nPred": nPred
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

    def parse_raw_result(self, raw_result):
        result = []
        for _, row in raw_result.iterrows():
            row_res = utils.parse_metadata(row.metadata)
            row_res["metadata"] = row.metadata
            row_res["prompt"] = row.prompt
            row_res["completion"] = self.remove_ending(row.choices[0]["text"])
            row_res["method"] = row_res["sampleMethod"] + row_res["numSamples"]
            row_res["label"] = self.remove_ending(row_res["label"])
            row_res["y_pred"] = self._get_pred(row_res["completion"])
            row_res["y_gt"] = self._get_gt(row_res["label"])     
            result.append(row_res)
            
            # evaluate each row
            row_eval = self._evaluate_row(row_res["y_gt"], row_res["y_pred"])
            for k, v in row_eval.items():
                row_res[k] = v
        result = pd.DataFrame(result)
        return result