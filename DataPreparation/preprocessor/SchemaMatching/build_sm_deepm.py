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

def build_deepm(root_data_dir, root_save_dir):
    print("build SM DeepM")
    
    data_dir = os.path.join(root_data_dir, "DeepM")
    save_dir = os.path.join(root_save_dir, "test_only", "DeepM")

    for d in os.listdir(data_dir):
        for file in os.listdir(os.path.join(data_dir, d)):
            if file.endswith("mapping.json"):
                with open(os.path.join(data_dir, d, file), "r") as f:
                    map_dict = json.load(f)
            elif file.endswith("source.csv"):
                source = pd.read_csv(os.path.join(data_dir, d, file), skiprows=1)
            elif file.endswith("target.csv"):
                target = pd.read_csv(os.path.join(data_dir, d, file))
            
        source.iloc[:5].to_csv(makedir([save_dir, d],"table1.csv"), index=False)
        target.iloc[:5].to_csv(makedir([save_dir, d],"table2.csv"), index=False)
        
        info = {}
        for match in map_dict["matches"]:
            info[match["source_column"]] = match["target_column"]
            
        new_info = {
            "old_headers": list(info.keys()),
            "alternative_headers": list(info.values())
        }
            
        with open(makedir([save_dir, d],"info.json"), "w") as f:
            json.dump(new_info, f, indent=4)