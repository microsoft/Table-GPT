import os
from tqdm import tqdm
from utils import makedir, is_good_text_column
import numpy as np
from multiprocessing import Pool
import pandas as pd

class BaseSynthesizer(object):
    def __init__(self):
        pass
    
    def synthesize_one(self, df_full, random_state, save_dir):
        raise Exception("Not Implemented")
    
    def run_one(self, args):
        file_data_dir, file_save_dir, seed = args
        df_full = pd.read_csv(file_data_dir, dtype=str)    
        self.synthesize_one(df_full, random_state=seed, save_dir=file_save_dir)
        
    def synthesize(self, data_dir, dataset, save_dir, max_size=None, random_state=1, n_jobs=1, batch_size=1024, mode=None):
        print("Processing", dataset)
        self.mode = mode
        full_file_list = sorted(os.listdir(os.path.join(data_dir, dataset)))
        if len(full_file_list) > max_size:
            np.random.seed(random_state)
            indices = np.random.permutation(len(full_file_list))[:max_size]
            file_list = [full_file_list[i] for i in indices]
        else:
            file_list = full_file_list
            
        args = []
        for i, file in enumerate(file_list):
            file_data_dir = os.path.join(data_dir, dataset, file)
            file_save_dir = os.path.join(save_dir, dataset, file[:-4])
            seed = random_state + i
            args.append((file_data_dir, file_save_dir, seed)) 
        
        n_batches = (len(args) - 1) // batch_size + 1
        
        for i in tqdm(range(n_batches)):
            batch = args[i*batch_size: (i+1)*batch_size]
            
            if n_jobs == 1:
                for arg in batch:
                    self.run_one(arg)
            else:
                with Pool(n_jobs) as pool:
                    pool.map(self.run_one, batch)
            

        