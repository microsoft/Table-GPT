import pandas as pd
import numpy as np
# clean movie3
def clean_movie3():
    # a-1 => 1
    df_path_1 = "raw/784datasets/movies3/csv_files/imdb.csv"
    df_path_2 = "raw/784datasets/movies3/csv_files/rotten_tomatoes.csv"
    df = pd.read_csv(df_path_1)
    new_id = [x.split("-")[1] for x in df["ID"]]
    df["ID"] = new_id
    df.to_csv(df_path_1, index=False)
    
    df = pd.read_csv(df_path_2)
    new_id = [x.split("-")[1] for x in df["ID"]]
    df["ID"] = new_id
    df.to_csv(df_path_2, index=False)
    
    
def clean_restaurant1():
    df_path_1 = "raw/784datasets/restaurants1/csv_files/yelp.csv"
    df_path_2 = "raw/784datasets/restaurants1/csv_files/zomato.csv"
    df = pd.read_csv(df_path_1)
    df["ID"] = np.arange(len(df)) + 1
    df.to_csv(df_path_1, index=False)
    
    df = pd.read_csv(df_path_2)
    df["ID"] = np.arange(len(df))
    df.to_csv(df_path_2, index=False)
    
def clean_movie2():
    df_path_1 = "raw/784datasets/movies2/csv_files/imdb.csv"
    df_path_2 = "raw/784datasets/movies2/csv_files/tmd.csv"
    label_path = "raw/784datasets/movies2/csv_files/labeled_data.csv"
    
    df1 = pd.read_csv(df_path_1, on_bad_lines="skip")
    df2 = pd.read_csv(df_path_2, on_bad_lines="skip")
    
    new_id = [int(x) for x in df1["ID"].values]
    df1["ID"] = new_id
    new_id = [int(x) for x in df2["ID"].values]
    df2["ID"] = new_id

    df1 = df1[~df1[" name"].isnull()]
    df2 = df2[~df2["title"].isnull()]
    
    gt = pd.read_csv(label_path, skiprows=5)
    
    lid_set = set(df1["ID"])
    rid_set = set(df2["ID"])
    mask = []
    for lid, rid in gt[["ltable.ID", "rtable.ID"]].values:
        if lid not in lid_set or rid not in rid_set:
            mask.append(False)
        else:
            mask.append(True)
    gt = gt[mask]
    
    df1.to_csv(df_path_1, index=False)
    df2.to_csv(df_path_2, index=False)
    gt.to_csv(label_path, index=False)

# clean_movie3()
# clean_restaurant1()
clean_movie2()