from .base_evaluator import BaseEvaluator

class HVMEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.answer_key = "column headers"
        
    def _evaluate_row(self, y_true, y_pred):
        count = 0
        for yt, yp in zip(y_true, y_pred):
            if yt == yp:
                count += 1
        res = {
            "acc": count / len(y_true)
        }
        return res

    def _compute_metric(self, res):
        acc = res["correct"].values.mean()
        metric = {
            "acc": acc
        }
        return metric