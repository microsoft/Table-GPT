# azureml-core of version 1.0.72 or higher is required
from azureml.core import Workspace, Dataset
import sys
import os
from datetime import date
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", nargs="+", default=None)
parser.add_argument("--save_dir", default=None)
parser.add_argument("--region", default="cu", choices=["eu", "cu"])
args = parser.parse_args()

for name in args.name:
    print("download", name)
    subscription_id = '19f75306-19b2-450f-a135-9045333bbb48'
    resource_group = 'babel'
    if args.region == "eu":
        workspace_name = 'babel-oai-east-us'
    elif args.region == "cu":
        workspace_name = 'babel-oai-south-central-us'
    else:
        raise Exception("wrong region")
        
    today = date.today().strftime("%m%d")
    if args.save_dir is None:
        args.save_dir = f'result_{today}'

    workspace = Workspace(subscription_id, resource_group, workspace_name)

    dataset = Dataset.get_by_name(workspace, name=name)
    paths = dataset.download(target_path=os.path.join(args.save_dir, 'preds'), overwrite=True)

    # rename
    old_path = paths[0]
    path_splits = list(os.path.split(old_path))
    folder = os.path.join(*path_splits[:-1])
    filename = path_splits[-1][:-6]
    fileext = "jsonl"
    new_path = os.path.join(folder, f"{name}.{fileext}")

    os.rename(old_path, new_path)