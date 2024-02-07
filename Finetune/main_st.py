import pandas as pd
import sys
import argparse
import utils

def remove_ending(name):
    if "-Size" in name:
        prefix, suffix = name.split("-Size")
    else:
        prefix = name
    return prefix

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", default=None)
parser.add_argument("--sample", default=None, type=float, help="our sample rate")
parser.add_argument("--size", default=None, nargs="+")
args = parser.parse_args()

full = pd.read_json(args.data_path, lines=True)

for size in args.size:
    data = full.iloc[:int(size)]
    name = args.data_path.strip("/").split("/")[-1]
    name = remove_ending(name)
    name = name.split("-ST-")[1]
    data.to_json(f"STFinetune-TrainData-FinalDatav4-{name}-Size_{len(data)}".replace(".", "_") + ".jsonl", orient='records', lines=True)

