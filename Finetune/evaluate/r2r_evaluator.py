from .base_evaluator import BaseEvaluator
import utils
import pandas as pd

class R2REvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__()
        self.answer_key = "output_value"
        
    def _evaluate_row(self, y_true, y_pred):
        correct = int(y_true == y_pred)
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
    
    def parse_raw_result(self, raw_result):
        result = []
        for _, row in raw_result.iterrows():
            row_res = utils.parse_metadata(row.metadata)
            row_res["metadata"] = row.metadata
            row_res["prompt"] = row.prompt
            row_res["completion"] = self.remove_ending(row.choices[0]["text"])
            row_res["method"] = row_res["sampleMethod"] + row_res["numSamples"]
            row_res["label"] = self.remove_ending(row_res["label"])
            row_res["prompt_completion"] = row_res["prompt"] + "\n" + row_res["completion"]
            row_res["y_pred"] = self._get_pred(row_res["completion"])
            row_res["y_gt"] = self._get_gt(row_res["label"])

            if row_res["benchmark"] == "TDE":
                if "benchmark-stackoverflow" in row_res["filename"]:
                    row_res["benchmark"] = "Stackoverflow"
                elif "unit" in row_res["filename"]:
                    row_res["benchmark"] = "BingQL-Unit"
                elif "benchmark-FF-Trifacta-GoogleRefine" in row_res["filename"]:
                    row_res["benchmark"] = "FF-GR-Trifacta"
                elif "benchmark-headcase" in row_res["filename"]:
                    row_res["benchmark"] = "Headcase"
                else:
                    row_res["benchmark"] = "BingQL-other"
            
            # evaluate each row
            row_eval = self._evaluate_row(row_res["y_gt"], row_res["y_pred"])
            for k, v in row_eval.items():
                row_res[k] = v
                
            result.append(row_res)
        result = pd.DataFrame(result)
        return result