import pandas as pd
import os
import json
from tqdm import tqdm
import sys
sys.path.append("../..")
from utils import makedir
import numpy as np
from copy import deepcopy
import json
import pandas as pd
import os
from .sql import Query
from collections import defaultdict
from tqdm import trange

def buil_wikisql(data_dir, root_save_dir):
    print("build NL2SQL wikisql")
    sql_path = os.path.join(data_dir, "wikisql/train.jsonl")
    table_path = os.path.join(data_dir, "wikisql/train.tables.jsonl")
    save_dir = os.path.join(root_save_dir, "train_only", "WikiSQL")

    sql_df = pd.read_json(sql_path, lines=True)
    table_df = pd.read_json(table_path, lines=True)

    table_df = table_df.set_index("id")
    count = 0
    pbar = trange(len(sql_df))
    table_count = defaultdict(int)
    for _, row in sql_df.iterrows():
        pbar.update(1)
        table = table_df.loc[row.table_id]
        df = pd.DataFrame(table.rows, columns=table.header)
        question = row.question
        sql = row.sql
        if len(sql.keys()) > 3:
            print(sql)
        query = str(Query(sel_index=sql["sel"], agg_index=sql["agg"], conditions=sql["conds"]))
        
        column_map = {}
        for i, c in enumerate(df.columns):
            column_map[f"col{i}"] = f"`{c}`"
        
        for k, v in column_map.items():
            query = query.replace(k, v)
        
        if table_count[row.table_id] > 1:
            continue
        
        info = {
            "table_id": row.table_id,
            "question": question,
            "label": str(query)
        }
        
        if len(df) > 3 and df.shape[1] < 15:
            count += 1
            table_count[row.table_id] += 1
            with open(makedir([save_dir, f"Table{count}"], "info.json"), "w") as f:
                json.dump(info, f, indent=4)
            df = df.iloc[:5]
            df.to_csv(makedir([save_dir, f"Table{count}"], "data.csv"), index=False)

