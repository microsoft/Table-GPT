import os

def makedir(dir_list, file=None):
    save_dir = os.path.join(*dir_list)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if file is not None:
        save_dir = os.path.join(save_dir, file)
    return save_dir

data_dir = "Magellan"
save_dir = makedir(["raw", "784datasets"])
for d in os.listdir(data_dir):
    print(d)
    os.system("tar -xf {} --directory {}".format(os.path.join(data_dir, d), save_dir))