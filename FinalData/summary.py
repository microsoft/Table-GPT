import pandas as pd
import utils

# version = "v4"
# data_path = f"VaryTrain{version}/VaryTrain-TrainData-FinalDatav4-tokens_4096-PerturbSample_0_2-Size_17909.jsonl"
# data = pd.read_json(data_path, lines=True)
# data["task"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["task"])

# for t, sub in data.groupby("task"):
#     print(t, len(sub))

version = "v4"
data_path = "TrainTestDataFinalCombinedv4/TestData-FinalDatav4-tokens_4096-All-CF_DI_ED_EM_MCCN_MCCS_MCRN_MCRS_R2RF_SM_TQ_CTA-Size_78273.jsonl"
data = pd.read_json(data_path, lines=True)
data["task"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["task"])
data["numSamples"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["numSamples"])
data["benchmark"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["benchmark"])
data["dataset"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["dataset"])
data = data[data["numSamples"] == '0']
data = data[data["task"] == "Row2RowFewshot"]


data["filename"] = data["metadata"].apply(lambda x: utils.parse_metadata(x)["filename"])
for _, row_res in data.iterrows():
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

for t, sub in data.groupby(["task", "benchmark"]):
    print(t, len(sub))


