import re
import json
from sklearn.metrics import f1_score
import numpy as np


class Evaluator(object):
    def __init__(self, task):
        self.task = task
        answer_keys = {
            "ColumnFinding": "result",
            "ColumnTypeAnnotation": "chosen_semantic_type",
            "DataImputation": "value",
            "Row2RowTransformation": "output_value",
            "TableQuestion": "answer",
            "EntityMatching": "answer",
            "MissingValueIdentification": ["missing_col", "row_id"],
            "ErrorDetection": "erroneous_cells",
            "SchemaMatching": "column_mappings",
        }
        evaluate_fns = {
            "EntityMatching": self.evaluate_em,
            "ErrorDetection": self.evaluate_ed,
            "ColumnFinding": self.evaluate_cf,
            "DataImputation": self.evaluate_di,
            "Row2RowTransformation": self.evaluate_r2r,
            "TableQuestion": self.evaluate_tq,
            "SchemaMatching": self.evaluate_sm,
            "ColumnTypeAnnotation": self.evaluate_cta,
            "MissingValueIdentification": self.evaluate_mvi,
        }

        self.answer_key = answer_keys[self.task]
        self.eval_fn = evaluate_fns[self.task]

    def compute_score(self, result):
        # extract prediction and label
        y_pred = result["prediction"].apply(
            lambda x: self.extract_json_answer(x, self.answer_key)
        )
        y_true = result["completion"].apply(
            lambda x: self.extract_json_answer(x, self.answer_key)
        )
        return self.eval_fn(y_true, y_pred)

    def extract_json_answer(self, text, answer_key):
        # extract answer from completion
        assert answer_key is not None
        pattern = r"{[^}]*}"  # Regex pattern to match strings inside curly braces while keeping the braces
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                result = json.loads(match)

                if type(answer_key) == list:
                    for key in answer_key:
                        if key in result:
                            return result[key]
                else:
                    if answer_key in result:
                        return result[answer_key]
            except:
                continue
        return "JSONParsingError"

    def evaluate_em(self, y_true, y_pred):
        y_true = y_true.apply(lambda x: int(x.lower() == "yes"))
        y_pred = y_pred.apply(lambda x: int(x.lower() == "yes"))
        f1 = f1_score(y_true, y_pred)
        return f1

    def evaluate_ed(self, y_true, y_pred):
        TP_count = 0
        FP_count = 0
        FN_count = 0

        def preprocess(y):
            if y == "JSONParsingError" or y is None:
                y = []
            elif type(y) == str:
                if y.lower() == "none":
                    y = []
                else:
                    y = [y]
            return set(y)

        for y_t, y_p in zip(y_true, y_pred):
            y_true_set = preprocess(y_t)
            y_pred_set = preprocess(y_p)
            tp_set = list(y_true_set.intersection(y_pred_set))[:1]  # there is only 1 gt

            nP = min(len(y_true_set), 1)
            nTP = min(len(tp_set), 1)
            nFP = 0
            for y_pred in y_pred_set:
                if y_pred not in y_true_set:
                    nFP += 1
            nFN = nP - nTP

            TP_count += len(tp_set)
            FP_count += nFP
            FN_count += nFN

        prec = TP_count / (TP_count + FP_count)
        recall = TP_count / (TP_count + FN_count)
        f1 = 2 * prec * recall / (prec + recall)
        return f1

    def evaluate_cf(self, y_true, y_pred):
        corrects = [
            int(str(y_t).lower() == str(y_p).lower())
            for y_t, y_p in zip(y_true, y_pred)
        ]
        acc = sum(corrects) / len(corrects)
        return acc

    def evaluate_di(self, y_true, y_pred):
        corrects = [
            int(str(y_t).lower() == str(y_p).lower())
            for y_t, y_p in zip(y_true, y_pred)
        ]
        acc = sum(corrects) / len(corrects)
        return acc

    def evaluate_r2r(self, y_true, y_pred):
        corrects = y_true == y_pred
        acc = corrects.mean()
        return acc

    def evaluate_tq(self, y_true, y_pred):
        corrects = [
            int(str(y_t).lower() == str(y_p).lower())
            for y_t, y_p in zip(y_true, y_pred)
        ]
        acc = sum(corrects) / len(corrects)
        return acc

    def evaluate_sm(self, y_true, y_pred):
        def parse_matching(label):
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

        recalls = []
        for y_t, y_p in zip(y_true, y_pred):
            y_t = parse_matching(y_t)
            y_p = parse_matching(y_p)
            # no rand
            count = 0
            for k in y_p.keys():
                if k in y_t and y_p[k] == y_t[k]:
                    count += 1
            if len(y_t) == 0:
                r = None
            else:
                r = count / len(y_t)
            recalls.append(r)
        return sum(recalls) / len(recalls)

    def evaluate_cta(self, y_true, y_pred):
        TP_count = 0
        FP_count = 0
        FN_count = 0

        for y_t, y_p in zip(y_true, y_pred):
            if str(y_t) == "None":
                y_t = []
                nP = 0
            else:
                nP = 1

            if str(y_p) != "None" and y_p == y_t:
                nTP = 1
            else:
                nTP = 0

            if str(y_p) == "None":
                nPP = 0
            else:
                nPP = 1

            nFP = nPP - nTP
            nFN = nP - nTP

            TP_count += nTP
            FP_count += nFP
            FN_count += nFN

        prec = TP_count / (TP_count + FP_count)
        recall = TP_count / (TP_count + FN_count)
        f1 = 2 * prec * recall / (prec + recall)
        return f1

    def evaluate_mvi(self, y_true, y_pred):
        corrects = [
            int(str(y_t).lower() == str(y_p).lower())
            for y_t, y_p in zip(y_true, y_pred)
        ]
        acc = sum(corrects) / len(corrects)
        return acc
