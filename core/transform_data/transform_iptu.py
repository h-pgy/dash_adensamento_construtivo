from core.read_data import iptu_gen
from core.utils.file_path import solve_path
import pandas as pd
import os
from .group_iptu import GroupbyQuadra
from config import GENERATED_DATA_FOLDER

class TransformAllIptu:
    
    def __init__(self, folder = GENERATED_DATA_FOLDER):
        
        self.iptus = iptu_gen() 
        self.transform = GroupbyQuadra()
        self.folder = folder
        
    def get_fname(self, df):
        
        ano = df['ano_arquivo'].unique()[0]
        fname = f'{ano}_quadras.parquet.gzip'
        
        fname = solve_path(fname, parent=self.folder)
        
        return fname
        
    def save_parquet(self, grouped, fname):
        
        grouped.to_parquet(fname,
              compression='gzip')
        
    def save_all_parquets(self):
        
        all_dfs = []
        for iptu in self.iptus:
            fname = self.get_fname(iptu)
            if os.path.exists(fname):
                print(f'Reading {fname}')
                grouped = pd.read_parquet(fname)
            else:
                print(f'Saving {fname}')
                grouped = self.transform(iptu)
                self.save_parquet(grouped, fname)
            
            all_dfs.append(grouped)
        
        final = pd.concat(all_dfs)
        
        return final
    
    
    def pipeline(self):
        
        fname = solve_path('quadra_all_years.parquet.gzip', self.folder)
        
        if os.path.exists(fname):
            print('Reading saved file')
            return pd.read_parquet(fname)
        
        final = self.save_all_parquets()
        self.save_parquet(final, fname)
        
        return final

    
    def __call__(self):
        
        return self.pipeline()