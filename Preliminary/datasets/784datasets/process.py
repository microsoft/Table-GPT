import pandas as pd
import os
import numpy as np

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def load_df(df_path):
    try:
        df = pd.read_csv(df_path)
    except:
        try:
            df = pd.read_csv(df_path, encoding="latin")
        except:
            print(d,t)
            raise
    return df

def stringfy(x):
    try:
        x_float = float(x)
        if float(x) == int(x):
            return str(int(x))
        else:
            return str(float(x))
    except:
        return str(x)

dataset = "784datasets"
info = pd.read_csv(os.path.join("raw", "{}_info.csv").format(dataset))
save_dir = makedir(["data", dataset])
name_dict = {}
for name, name_l, name_r in info[["Name", "Left", "Right"]].values:
    name_dict[name.lower().replace(" ", "")] = (name_l.lower().replace(" ", ""), name_r.lower().replace(" ", ""))

for d in os.listdir(os.path.join("raw", dataset)):
    print(d)
    left = None
    right = None
    for t in os.listdir(os.path.join("raw", dataset, d, "csv_files")):
        # get left and right        
        name_l, name_r = name_dict[d.lower().replace("_", "")]
        if t in ["candset.csv", "labeled_data.csv"]:
            continue
  
        df = load_df(os.path.join("raw", dataset, d, "csv_files", t))    
                
        # rename id column
        id_column = df.columns[0]
        df = df.rename(columns={id_column:"id"})
        assert("id" not in df.columns[1:])

        # get left right table
        t_str = t[:-4].lower().replace("_", "")
        if t_str == name_l:
            left = df
        elif t_str == name_r:
            right = df
        else:
            print(d, t_str, name_l, name_r)
            raise
    
    # reset id column
    left_id_map = {stringfy(old_id): i for i, old_id in enumerate(left["id"].values)}
    right_id_map = {stringfy(old_id): i for i, old_id in enumerate(right["id"].values)}
    
    # reset id
    left["id"] = np.arange(len(left))
    right["id"] = np.arange(len(right))
    left.to_csv(makedir([save_dir, d], "tableA.csv"), index=False)
    right.to_csv(makedir([save_dir, d], "tableB.csv"), index=False)
    
    # load labeled data
    try:
        data = pd.read_csv(os.path.join("raw", dataset, d, "csv_files", "labeled_data.csv"), skiprows=5)
    except:
        data = pd.read_csv(os.path.join("raw", dataset, d, "csv_files", "labeled_data.csv"), skiprows=5, encoding="latin")
    
    # rename ltable ID
    alias_l = ["ltable.ID", "ltable.int_id", "ltable.Label", "ltable.id", "ltable.Product_id", "ltable.record_id", "ltable.Id", "ltable.Sno", "ltable._id"]
    alias_r = ["rtable.ID", "rtable.int_id", "rtable.Label", "rtable.id", "rtable.Product_id", "rtable.record_id", "rtable.Id", "rtable.Sno", "rtable._id"]
    for lid in alias_l:
        if lid in data.columns:
            data = data.rename(columns={lid:"ltable_id"})
            break
        
    if "ltable_id" not in data.columns:
        print(d,t,data.columns)
        raise

    for rid in alias_r:
        if rid in data.columns:
            data = data.rename(columns={rid:"rtable_id"})
            break
        
    if "rtable_id" not in data.columns:
        print(d,t,data.columns)
        raise
    
    alias_label = ["gold", "product_is_match", "gold_label", "match_label", "Gold", "is_match", "label", "class_label"]
    for name in alias_label:
        if name in data.columns:
            data = data.rename(columns={name:"label"})
    data = data[["ltable_id", "rtable_id", "label"]]
    
    new_data = []
    for lid, rid, y in data.values:
        if stringfy(lid) not in left_id_map:
            print(d, "Error: {} not in left table".format(lid))
            raise
        if stringfy(rid) not in right_id_map:
            print(d, "Error: {} not in right table".format(right))
            raise
        
        new_data.append([left_id_map[stringfy(lid)], right_id_map[stringfy(rid)], y])
    new_data = pd.DataFrame(new_data, columns=["ltable_id", "rtable_id", "label"])
    data = new_data
    
    data.to_csv(makedir([save_dir, d], "labeled_data.csv"), index=False)
    
    np.random.seed(1)
    indices = np.random.permutation(len(data))
    N = len(data)
    N_test = int(N * 0.2)
    test_indices = indices[:N_test]
    val_indices = indices[N_test:N_test+N_test]
    train_indices = indices[N_test+N_test:]
    
    train_df = data.iloc[train_indices]
    val_df = data.iloc[val_indices]
    test_df = data.iloc[test_indices]
    
    train_df.to_csv(makedir([save_dir, d], "train.csv"), index=False)
    val_df.to_csv(makedir([save_dir, d], "val.csv"), index=False)
    test_df.to_csv(makedir([save_dir, d], "test.csv"), index=False)
    
    # test join
    try:
        data = pd.merge(data, left, left_on="ltable_id", right_on="id")
        merge = pd.merge(data, right, left_on="rtable_id", right_on="id")
        assert(len(merge) > 0)
    except Exception as e:
        print(d, str(e))
        raise
        
        
        

    