from utils import train_test_split_synthetic, train_test_split, random_sample
import os
import argparse
import utils
from shutil import copytree
from multiprocessing import Pool

def copy_data(paths):
    old_dir, new_dir = paths
    copytree(old_dir, new_dir)

parser = argparse.ArgumentParser()
parser.add_argument("version")
parser.add_argument("--save_dir", default="../Finetune/data")
parser.add_argument("--n_test", default=1000, type=int)
parser.add_argument("--seed", default=1, type=int)
parser.add_argument("--n_jobs", default=-1, type=int)
args = parser.parse_args()

if args.n_jobs < 0:
    args.n_jobs = os.cpu_count()

# data sources
source_dir = os.path.join("source", f"source_v{args.version}")
root_save_dir = os.path.join(args.save_dir, f"data_v{args.version}")

tasks = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
for task in tasks:
    print("Processing task", task)
    for mode in ["train", "test_only", "train_only"]:
        data_dir = os.path.join(source_dir, task, mode)
        
        if not os.path.exists(data_dir):
            continue

        for dataset in sorted(os.listdir(data_dir)):
            print("- Processing dataset", dataset)
            dataset_dir = os.path.join(data_dir, dataset)
            tables = sorted(os.listdir(dataset_dir))
            
            if mode == "train":
                test_tables, train_tables = train_test_split(tables, args.n_test, seed=args.seed)
            elif mode == "test_only":
                train_tables = None
                if dataset == "ExcelSynthetic":
                    test_tables = random_sample(tables, args.n_test, seed=args.seed)
                else:
                    test_tables = tables
            else:
                train_tables = tables
                test_tables = None
            
            paths = []
            if train_tables is not None:
                for i, table in enumerate(train_tables):
                    old_dir = os.path.join(dataset_dir, table)
                    new_dir = utils.makedir([root_save_dir, task, "train", dataset], table)
                    paths.append((old_dir, new_dir))
            
            if test_tables is not None:
                for i, table in enumerate(test_tables):
                    old_dir = os.path.join(dataset_dir, table)
                    new_dir = utils.makedir([root_save_dir, task, "test", dataset], table)
                    paths.append((old_dir, new_dir))
                    
            with Pool(args.n_jobs) as pool:
                pool.map(copy_data, paths)
                
utils.save_version(root_save_dir, args.version)