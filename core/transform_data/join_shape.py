import pandas as pd
import os

from core.utils.file_path import solve_path
from .transform_iptu import TransformAllIptu
from core.read_data import read_shp_quadras
from config import GENERATED_DATA_FOLDER
import geopandas as gpd

class JoinShp:


    def __init__(self)->None:

        self.get_setores_iptu = TransformAllIptu()

        self.fname = solve_path('setores_geodataframe.shp', GENERATED_DATA_FOLDER)

    def get_shape_setores(self)->gpd.GeoDataFrame:

        shp_setores = read_shp_quadras()

        return shp_setores

    def create_setores_col(self, shp_setores:gpd.GeoDataFrame)->None:

        shp_setores['setor'] = shp_setores['st_codigo']
    
    def select_cols_shp(self, shp_setores:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        return shp_setores[['setor', 'geometry']]

    def merge(self, shp_setores:gpd.GeoDataFrame, setores_iptu:pd.DataFrame)->pd.DataFrame:

        final = pd.merge(setores_iptu, shp_setores, how='left')
        
        return final

    def clean_ano(self, final:pd.DataFrame)->None:

        final.drop('ano_y', axis=1, inplace=True)
        final.rename({'ano_x' : 'ano'}, axis=1, inplace=True)

    def convert_geodf(self, merged:pd.DataFrame)->gpd.GeoDataFrame:

        geodf = gpd.GeoDataFrame(merged, geometry='geometry')
        geodf = geodf.set_crs(epsg=31983)
        geodf = geodf.to_crs(epsg=4326)

        return geodf
    
    def pipeline(self)->None:

        if os.path.exists(self.fname):
            return gpd.read_file(self.fname)
        
        setores_iptu = self.get_setores_iptu()
        #setores_iptu = setores_iptu[setores_iptu['ano_y']==2022]
        shp_setores = self.get_shape_setores()
        self.create_setores_col(shp_setores)
        shp_setores = self.select_cols_shp(shp_setores)
        final = self.merge(shp_setores, setores_iptu)
        self.clean_ano(final)
        final = self.convert_geodf(final)

        final.to_file(self.fname)

        return final

    def __call__(self):

        return self.pipeline()

    

    

