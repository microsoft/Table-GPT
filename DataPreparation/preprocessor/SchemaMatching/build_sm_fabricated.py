import pandas as pd
import os
import json

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir


def listdir(d):
    return [f for f in os.listdir(d) if f[0] != "."]

def build_fabricated(root_data_dir, root_sve_dir):
    print("build SM Fabricated")
    data_dir = os.path.join(root_data_dir, "Fabricated")
    save_dir = os.path.join(root_sve_dir, "test_only", "Fabricated")
    count_bad = 0
    for b in listdir(data_dir):
        for t in listdir(os.path.join(data_dir, b)):
            for d in listdir(os.path.join(data_dir, b, t)):
                dataset_dir = os.path.join(data_dir, b, t)
                for file in listdir(os.path.join(dataset_dir, d)):
                    if file.endswith("mapping.json"):
                        with open(os.path.join(dataset_dir, d, file), "r") as f:
                            map_dict = json.load(f)
                    elif file.endswith("source.csv"):
                        source = pd.read_csv(os.path.join(dataset_dir, d, file))
                    elif file.endswith("target.csv"):
                        target = pd.read_csv(os.path.join(dataset_dir, d, file))
                
                name = "_".join([b, t, d])
                source = source.iloc[:10]
                target = target.iloc[:10]

            
                info = {}
                check = False
                for match in map_dict["matches"]:
                    info[match["source_column"]] = match["target_column"]
                    if match["source_column"] not in source.columns:
                        check = True
                        count_bad += 1
                    if match["target_column"] not in target.columns:
                        check = True
                        count_bad += 1
                
                if check:
                    continue
                    
                source.iloc[:5].to_csv(makedir([save_dir, name],"table1.csv"), index=False)
                target.iloc[:5].to_csv(makedir([save_dir, name],"table2.csv"), index=False)
                
                new_info = {
                    "old_headers": list(info.keys()),
                    "alternative_headers": list(info.values())
                }
                with open(makedir([save_dir, name],"info.json"), "w") as f:
                    json.dump(new_info, f, indent=4)

    print(count_bad)