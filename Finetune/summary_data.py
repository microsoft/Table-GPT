import sys
import pandas as pd
import utils

data = pd.read_json(sys.argv[1], lines=True)

meta = data["metadata"].apply(lambda x: utils.parse_metadata(x))

meta_df = pd.DataFrame(meta.tolist())

summary = meta_df.groupby(["task", "benchmark", "sampleMethod", "numSamples", "seed"]).agg(len)
summary.to_excel("summary.xlsx")