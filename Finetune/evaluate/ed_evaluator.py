from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import utils
import os
from .base_evaluator import BaseEvaluator
from multiprocessing import Pool

class EDEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.group_keys = ["method", "benchmark", "seed"]
        self.merge_keys = ["method", "benchmark"]
        self.answer_key = "erroneous_cells"
    
    def preprocess(self, y):
        if y == "JSONParsingError" or y is None:
            y = []
        elif type(y) == str:
            if y.lower() == "none":
                y = []
            else:
                y = [y]
        return set(y)
    
    def _evaluate_row(self, y_true, y_pred):
        y_true_set = self.preprocess(y_true)
        y_pred_set = self.preprocess(y_pred)        
    
        # extractly correct
        tp_set = y_true_set.intersection(y_pred_set)
        correct = int(y_pred_set == y_true_set)
        res = {
            "correct": correct,
            "nTP": len(tp_set),
            "nFP": len(y_pred_set) - len(tp_set),
            "nFN": len(y_true_set) - len(tp_set),
            "nGT": len(y_true_set),
            "nPred": len(y_pred_set)
        }
        return res
    
    def _evaluate_row_excel(self, y_true, y_pred):
        # extractly correct
        y_true_set = self.preprocess(y_true)
        y_pred_set = self.preprocess(y_pred)
        tp_set = list(y_true_set.intersection(y_pred_set))[:1]
        # correct = int(y_pred_set == y_true_set)
        
        if len(y_true_set) == 0:
            correct = int(len(y_pred_set) == 0)
        else:
            correct = int(len(tp_set) == 1)
            
        if len(y_true_set) == 0:
            nP = 0
        else:
            nP = 1
        nFP = 0
        for y_pred in y_pred_set:
            if y_pred not in y_true_set:
                nFP += 1
            
        res = {
            "correct": correct,
            "nTP": len(tp_set),
            "nFP": nFP,
            "nFN": nP - len(tp_set),
            "nGT": nP,
            "nPred": len(y_pred_set)
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

            if "ExcelReal" in row_res["benchmark"] or "WebReal" in row_res["benchmark"]:
                row_eval = self._evaluate_row_excel(row_res["y_gt"], row_res["y_pred"])
            else:
                # evaluate each row
                row_eval = self._evaluate_row(row_res["y_gt"], row_res["y_pred"])
            for k, v in row_eval.items():
                row_res[k] = v
                
            result.append(row_res)
        result = pd.DataFrame(result)
        return result