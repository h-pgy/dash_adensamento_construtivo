from core.read_data import iptu_gen
from core.utils.file_path import solve_path
import pandas as pd
import os
from .group_iptu import GroupbySetor
from config import GENERATED_DATA_FOLDER, IPTU_YEARS

class TransformAllIptu:
    
    def __init__(self, folder:str = GENERATED_DATA_FOLDER, years:list=IPTU_YEARS)->None:
        
        self.iptus = iptu_gen() 
        self.transform = GroupbySetor()
        self.folder = folder
        self.years = years

    def extract_ano_df(self, df:pd.DataFrame)->str:
        
        ano = df['ano_arquivo'].unique()[0]
        return ano

    def get_fname(self, ano:int)->str:
        
        
        fname = f'{ano}_setores.parquet.gzip'
        fname = solve_path(fname, parent=self.folder)
        
        return fname
        
    def save_parquet(self, grouped, fname):
        
        grouped.to_parquet(fname,
              compression='gzip')

    def read_parquet(self, fname:str)->pd.DataFrame:

        return pd.read_parquet(fname)
        
    def save_all_parquets(self, all_dfs:list):
        
        for iptu in self.iptus:
            ano = self.extract_ano_df(iptu)
            fname = self.get_fname(ano)
            print(f'Saving {fname}')
            grouped = self.transform(iptu)
            self.save_parquet(grouped, fname)
            
            all_dfs.append(grouped)

    def read_all_parquets(self)->list:

        all_data = []
        for ano in self.years:
            fname = self.get_fname(ano)
            try:
                grouped = self.read_parquet(fname)
                all_data.append(grouped)
            except FileNotFoundError:
                return []
        return all_data

            
    def clean_year_col(self, df:pd.DataFrame)->None:

        df.rename({'ano_x' : 'ano'}, axis=1, inplace=True)
        df.drop('ano_y', axis=1, inplace=True)
    
    def pipeline(self):
        
        fname = solve_path('setores_all_years.parquet.gzip', self.folder)
        
        if os.path.exists(fname):
            print('Reading saved file')
            return pd.read_parquet(fname)
        
        all_data = self.read_all_parquets()

        if len(all_data)<1:
            self.save_all_parquets(all_data)

        final = pd.concat(all_data)
        self.clean_year_col(final)
        self.save_parquet(final, fname)

        
        return final
    
    def __call__(self):
        
        return self.pipeline()