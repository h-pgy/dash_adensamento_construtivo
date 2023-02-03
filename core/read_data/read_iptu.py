import pandas as pd
import os
from typing import Generator
from core.utils.file_path import list_files
from config import IPTU_DATA_FOLDER

class IptuCsvReader:
    
    
    def lst_iptu_csvs(self):

        return list_files(IPTU_DATA_FOLDER, extension='csv')

    def extract_year(self, fpath:str)->int:

        fname = os.path.split(fpath)[-1]
        return int(fname[-8:-4])


    def input_year(self, df:pd.DataFrame, fpath:str)->None:

        year = self.extract_year(fpath)
        df['ano_arquivo'] = year

    def read_csv(self, fpath:str)->pd.DataFrame:


        try:
            df = pd.read_csv(fpath, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(fpath, sep=';', encoding='latin-1')

        self.input_year(df, fpath)

        return df
    
    def csv_gen(self)->Generator[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        
        csv_lst = self.lst_iptu_csvs()
        
        for csv in csv_lst:
            yield self.read_csv(csv)
            
    def __call__(self)->Generator[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        
        return self.csv_gen()