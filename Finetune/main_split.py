import pandas as pd
import sys
import utils

print(sys.argv[1])
df = pd.read_json(sys.argv[1], lines=True)

df["benchmark"] = df["metadata"].apply(lambda x: utils.parse_metadata(x)["benchmark"])

name = sys.argv[1].split("/")[-1]

save_dir = "/".join(sys.argv[1].split("/")[:-1])

for benchmark, sub in df.groupby(by="benchmark"):
    name = name.split("-Size")[0]
    jsonl_save_dir = utils.makedir([save_dir], f"{name}-{benchmark}-Size_{len(sub)}.jsonl")
    columns = [x for x in sub.columns if x != "benchmark"]
    sub[columns].to_json(jsonl_save_dir, orient='records', lines=True)