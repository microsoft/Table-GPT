import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--data_path", default=None)
parser.add_argument("--flan_path", default="data/FlanTrainDataShuffled500k.jsonl")
parser.add_argument("--ratio", default=None, type=float, help="flan: our")
parser.add_argument("--sample", default=None, type=float, help="our sample rate")
args = parser.parse_args()


data = pd.read_json(args.data_path, lines=True)
if args.sample is not None:
    n_data = int(len(data) * args.sample)
    data = data.iloc[:n_data]
    
flan = pd.read_json(args.flan_path, lines=True)
flan_size = int(len(data) * args.ratio)
flan = flan.iloc[:flan_size]

mix = pd.concat([data, flan], axis=0).sample(frac=1, random_state=1, axis=0)

name = f"TrainData_FlanMixed_Ratio{args.ratio}" 
if args.sample is not None:
    name += f"_Sample{args.sample}"
name += "_" + args.data_path.split("TrainData-")[-1][:-6]
name += f"_Our{len(data)}_Flan{len(flan)}"

mix.to_json(f"{name}.jsonl", orient='records', lines=True)