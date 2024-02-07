import pandas as pd
import utils

version = "v4"
data_path = f"VaryTrain{version}/VaryTrain-TrainData-FinalDatav4-tokens_4096-PerturbSample_0_2-Size_17909.jsonl"

def remove_perturb(data):
    non_perturb_mask = ["colPerturbSeed" not in x for x in data["metadata"].values]
    perturb_mask = ["colPerturbSeed" in x for x in data["metadata"].values]
    return data[non_perturb_mask], data[perturb_mask]

def no_col_perturb():
    data = pd.read_json(data_path, lines=True)
    no_perturn, _ = remove_perturb(data)
    save_path = utils.makedir(["Ablationv4"], "Ablation-NoColPerturb-TrainData-FinalDatav4-tokens_4096-Size_13439.jsonl")
    utils.save_as_jsonl(no_perturn, save_path)
    
no_col_perturb()