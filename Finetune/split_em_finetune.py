import pandas as pd
import os
import sys
import utils

data = pd.read_json(sys.argv[1], lines=True)
mask = [utils.parse_metadata(x)["benchmark"] == "stanford" for x in data["metadata"].values]
data = data[mask]
data["dataset"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["dataset"])

# for dataset, sub in data.groupby(by="dataset"):  
#     utils.save_as_jsonl(sub.drop(columns="dataset"), f"TrainData-EMFinetune-{dataset}-Size{len(sub)}.jsonl")

for dataset, sub in data.groupby(by="dataset"):  
    utils.save_as_jsonl(sub.drop(columns="dataset"), f"TestData-EMFinetune-{dataset}-Size{len(sub)}.jsonl")
