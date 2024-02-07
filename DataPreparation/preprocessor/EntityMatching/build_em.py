import os
from shutil import copytree

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

def build_em(data_dir, save_dir):
    copytree(os.path.join(data_dir, "stanford"), makedir([save_dir, "test_only"], "stanford"))
    copytree(os.path.join(data_dir, "stanfordOriginal"), makedir([save_dir, "test_only"], "stanfordOriginal"))
    copytree(os.path.join(data_dir, "784datasets"), makedir([save_dir, "train_only"], "784datasets"))