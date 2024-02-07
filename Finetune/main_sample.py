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
parser.add_argument("--size", default=None, type=int)
parser.add_argument("--save_dir", default=None)
parser.add_argument("--shuffle", action="store_true", default=False)
args = parser.parse_args()

data = pd.read_json(args.data_path, lines=True)

if args.shuffle:
    data = data.sample(frac=1, random_state=1)

if args.size is not None:
    n_data = args.size
else:
    n_data = int(len(data) * args.sample)
data = data.iloc[:n_data]

name = args.data_path.strip("/").split("/")[-1]
name = remove_ending(name)

if args.save_dir is not None:
    data.to_json(utils.makedir([args.save_dir], f"{name}_Sample{args.sample}_Size{len(data)}".replace(".", "_") + ".jsonl", orient='records', lines=True))
else:
    data.to_json(f"{name}_Sample{args.sample}_Size{len(data)}".replace(".", "_") + ".jsonl", orient='records', lines=True)

