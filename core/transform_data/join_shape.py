import pandas as pd
import os

from core.utils.file_path import solve_path
from core.transform_data import transform_iptu
from core.read_data import read_shp_quadras
from config import GENERATED_DATA_FOLDER

class JoinShp:


    def __init__(self):

        self.get_quadras_iptu = transform_iptu

        self.fname = solve_path('quadras_geodataframe.parquet.gzip', GENERATED_DATA_FOLDER)

    def get_shape_quadras(self):

        shp_quadras = read_shp_quadras()

        return shp_quadras

    def create_quadras_col(self, shp_quadras):

        shp_quadras['quadra'] = shp_quadras['st_codigo']
    
    def select_cols_shp(self, shp_quadras):

        return shp_quadras[['quadra', 'geometry']]

    def merge(self, shp_quadras, quadras_iptu):

        final = pd.merge(quadras_iptu, shp_quadras, how='left')
        
        return final

    def save_parquet(self, df, fname):
        
        df.to_parquet(fname,
              compression='gzip')

    
    def pipeline(self):

        if os.path.exists(self.fname):
            print('Reading saved file')
            return pd.read_parquet(self.fname)
        
        quadras_iptu = self.get_quadras_iptu()
        quadras_iptu = quadras_iptu[quadras_iptu['ano_y']==2022]
        shp_quadras = self.get_shape_quadras()
        self.create_quadras_col(shp_quadras)
        shp_quadras = self.select_cols_shp(shp_quadras)
        final = self.merge(shp_quadras, quadras_iptu)
        #self.save_parquet(final, self.fname)

        return final

    def __call__(self):

        return self.pipeline()

    

    

