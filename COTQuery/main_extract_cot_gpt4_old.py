import pandas as pd

import os
import sys
sys.path.append("../Finetune")
import utils
import argparse
import json
import re

def extract_json_answer(text, answer_key):
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

parser = argparse.ArgumentParser()
parser.add_argument("version", default=None)
parser.add_argument("--data_dir", default="data")
parser.add_argument("--mode", default="train")
parser.add_argument("--temperature", type=float, default=0.0)
parser.add_argument("--n_jobs", type=int, default=8)
args = parser.parse_args()

pred_path = os.path.join(args.data_dir, f"cot_data_v{args.version}", "query_data", args.mode, "preds", "modelG4_vanilla.jsonl") 
save_dir = f"data/cot_data_v{args.version}"

print(pred_path)

preds = pd.read_json(pred_path, lines=True)

cot_data = []
count_uncomplete = 0

visited = {}
for _, row in preds.iterrows():

    meta = utils.parse_metadata(row["metadata"])
    raw_cot = row.choices[0]["text"]
    if meta["task"] == "EntityMatching":
        key = (meta["benchmark"], meta["dataset"], meta["lrid"])
    else:
        key = (meta["benchmark"], meta["dataset"])
    
    if key in visited:
        continue
    
    cot = raw_cot
    
    row_data = {
        "task": meta["task"],
        "benchmark": meta["benchmark"],
        "dataset": meta["dataset"],
        "cot": cot
    }
    
    if meta["task"] == "EntityMatching":
        row_data["lrid"] = meta["lrid"]
    
    visited[key] = row["metadata"]
    cot_data.append(row_data)


cot_data = pd.DataFrame(cot_data)

for (task, benchmark, dataset), group in cot_data.groupby(["task", "benchmark", "dataset"]):
    group.to_csv(utils.makedir([save_dir, "cot", task, args.mode, benchmark, dataset], "data.csv"), index=False)

    


