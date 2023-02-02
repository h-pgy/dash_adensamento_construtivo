import pandas as pd
import os
from core.utils.file_path import list_files
from config import IPTU_DATA_FOLDER

class IptuCsvReader:
    
    
    def lst_iptu_csvs(self):

        return list_files(IPTU_DATA_FOLDER, extension='csv')

    def extract_year(self, fpath):

        fname = os.path.split(fpath)[-1]
        return int(fname[-8:-4])


    def input_year(self, df, fpath):

        year = self.extract_year(fpath)
        df['ano_arquivo'] = year

    def read_csv(self, fpath):


        try:
            df = pd.read_csv(fpath, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(fpath, sep=';', encoding='latin-1')

        self.input_year(df, fpath)

        return df
    
    def csv_gen(self):
        
        csv_lst = self.lst_iptu_csvs()
        
        for csv in csv_lst:
            yield self.read_csv(csv)
            
    def __call__(self):
        
        return self.csv_gen()