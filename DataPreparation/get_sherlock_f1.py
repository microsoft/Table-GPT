import pandas as pd
import os
from sklearn.metrics import f1_score
import numpy as np

def evaluate_cta(y_true, y_pred):
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

pred = pd.read_csv(os.path.join("resources/resources_v11", "ColumnTypeAnnotation", "Sherlock", "Sherlock_pred.csv"))["y_pred"].values
true = pd.read_parquet(os.path.join("resources/resources_v11", "ColumnTypeAnnotation", "Sherlock", "test_labels.parquet"))["type"].values

np.random.seed(1)
sample_indices = np.random.permutation(len(true))[:1000]

y_pred = pred[sample_indices]
y_true = true[sample_indices]
f1 = evaluate_cta(y_true, y_pred)
print(f1)

print(f1_score(y_true, y_pred, average="weighted"))

# data = pd.read_parquet(os.path.join("resources/resources_v11", "ColumnTypeAnnotation", "Sherlock", "test_values.parquet"))
# print(len(data))
