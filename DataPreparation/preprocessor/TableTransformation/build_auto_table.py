import os
from shutil import copytree

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def build_auto_table(data_dir, save_dir):
    copytree(os.path.join(data_dir, "ATBench"), makedir([save_dir, "test_only"], "ATBench"))