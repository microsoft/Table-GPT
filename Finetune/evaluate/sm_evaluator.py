from .base_evaluator import BaseEvaluator
import numpy as np

class SMEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.answer_key = "column_mappings"
        
    def parse_matching(self, label):
        gt = {}
        if type(label) != list:
            return gt
        for x in label:
            if len(x) != 2:
                # print(x)
                continue
            source, target = x
            source = source.strip()
            target = target.strip()
            if len(target) == 0:
                continue
            gt[source] = target
        return gt
        
    def _evaluate_row(self, y_true, y_pred):
        y_true = self.parse_matching(y_true)
        y_pred = self.parse_matching(y_pred)
        # no rand
        count = 0
        for k in y_pred.keys():
            if k in y_true and y_pred[k] == y_true[k]:
                count += 1
        if len(y_true) == 0:
            recall = None
        else:
            recall = count / len(y_true)
        res = {
            "recall": recall
        }
        return res
    
    def _compute_metric(self, res):
        acc = res["recall"].values.mean()
        metric = {
            "recall": acc
        }
        return metric