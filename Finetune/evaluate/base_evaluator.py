from collections import defaultdict
import numpy as np
import pandas as pd
import utils
import os
import time
from multiprocessing import Pool
import re
import json

class BaseEvaluator(object):
    def __init__(self):
        self.group_keys = ["method", "benchmark", "dataset", "seed"]
        self.merge_keys = ["method", "benchmark", "dataset"]
        self.answer_key = None
    
    def _compute_metric(self, res) -> dict:
        # return a dict of evaluation metrics
        raise Exception("Not implemented")

    def _get_pred(self, completion):
        return self.extract_json_answer(completion, self.answer_key)
    
    def _get_gt(self, label):
        gt = self.extract_json_answer(label, self.answer_key)
        if gt == "JSONParsingError":
            print(label)
            raise Exception("Parsing Error on ground truth")
        return gt
    
    def _evaluate_row(self, y_true, y_pred) -> dict:
        raise Exception("Not implemented")
    
    def extract_json_answer(self, text, answer_key):
        assert answer_key is not None
        pattern = r'{[^}]*}'  # Regex pattern to match strings inside curly braces while keeping the braces
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                result = json.loads(match)
                if answer_key in result:
                    return result[answer_key]
            except:
                continue
        return "JSONParsingError"
        
    def remove_ending(self, completion):
        while True:
            if completion.endswith(" END"):
                completion = completion[:-4]
            else:
                break
        return completion.strip()
    
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
            
            # evaluate each row
            row_eval = self._evaluate_row(row_res["y_gt"], row_res["y_pred"])
            for k, v in row_eval.items():
                row_res[k] = v
                
            result.append(row_res)
        result = pd.DataFrame(result)
        return result
    
    def evaluate_one_case(self, case):
        group_key, group_df = case
        metric_group = self._compute_metric(group_df)
        return group_key, metric_group
    
    def save_debug(self, result, debug_dir):
        for (benchmark, seed, method), group_df in result.groupby(["benchmark", "seed", "method"]):
            group_df.to_csv(utils.makedir([debug_dir], f"{benchmark}_{method}_{seed}.csv"), index=False)
    
    def evaluate_by_group(self, result, group_keys, n_jobs=1):
        groups = list(result.groupby(group_keys))
        # evaluate result for each group
        if n_jobs == 1:
            eval_results = [self.evaluate_one_case(case) for case in groups]
        else:
            with Pool(n_jobs) as pool:
                eval_results = pool.map(self.evaluate_one_case, groups)
        
        group_keys = pd.DataFrame([key for key, _ in eval_results], columns=group_keys)
        group_metric = pd.DataFrame([metric for _, metric in eval_results])
        eval_results = pd.concat([group_keys, group_metric], axis=1)
        return eval_results
        
    def evaluate(self, raw_result, debug_dir=None, n_jobs=1, random_state=1):
        np.random.seed(random_state)
        # parse result
        result = self.parse_raw_result(raw_result)

        if debug_dir is not None:
            self.save_debug(result, debug_dir)

        # evaluate by groups
        eval_results = self.evaluate_by_group(result, self.group_keys, n_jobs=n_jobs)
        
        # # merge results from same seed
        merge_results = eval_results.groupby(self.merge_keys, as_index=False).agg(lambda x: list(x))
        
        # compute average
        avg_results = eval_results.groupby(self.merge_keys, as_index=False).mean().sort_values(by=self.merge_keys)
        return avg_results, merge_results