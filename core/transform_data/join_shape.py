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

    def pivot_setores_iptu(self, df:pd.DataFrame)->pd.DataFrame:

        pivotado = df.pivot(index='setor', columns='ano', 
                                            values=[
                                                'sum_area_construida', 
                                                'mean_valor_do_m2_do_terreno',
                                                'mean_quantidade_de_pavimentos'
                                                ]
                                            )
        pivotado = pivotado.reset_index()
        pivotado.rename({'' : 'setor'},axis=1, inplace=True)

        return pivotado

    def solve_pivoted_column(self, df:pd.DataFrame)->pd.DataFrame:

        dfs = []
        for index in ['sum_area_construida', 'mean_valor_do_m2_do_terreno', 'mean_quantidade_de_pavimentos']:
            tmp = df[index]
            rename = {ano : f'{index}_{ano}' for 
                    ano in tmp.columns}
            tmp.rename(rename, axis=1, inplace=True)
            dfs.append(tmp)

        dfs.append(df['setor'])
        df = pd.concat(dfs, axis=1, ignore_index=False)

        return df

    def get_shape_setores(self)->gpd.GeoDataFrame:

        shp_setores = read_shp_quadras()

        return shp_setores

    def create_setores_col(self, shp_setores:gpd.GeoDataFrame)->None:

        shp_setores['setor'] = shp_setores['st_codigo']
    
    def select_cols_shp(self, shp_setores:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        return shp_setores[['setor', 'geometry']]

    def merge(self, shp_setores:gpd.GeoDataFrame, setores_iptu:pd.DataFrame)->pd.DataFrame:

        final = pd.merge(shp_setores, setores_iptu, how='left').fillna(0)
        
        return final

    def convert_geodf(self, merged:pd.DataFrame)->gpd.GeoDataFrame:

        geodf = gpd.GeoDataFrame(merged, geometry='geometry')
        geodf = geodf.set_crs(epsg=31983)
        geodf = geodf.to_crs(epsg=4326)

        return geodf
    
    def pipeline(self)->None:

        #if os.path.exists(self.fname):
        #    return gpd.read_file(self.fname)
        
        setores_iptu = self.get_setores_iptu()
        setores_iptu = self.pivot_setores_iptu(setores_iptu) 
        setores_iptu = self.solve_pivoted_column(setores_iptu)
        shp_setores = self.get_shape_setores()
        self.create_setores_col(shp_setores)
        shp_setores = self.select_cols_shp(shp_setores)
        final = self.merge(shp_setores, setores_iptu)
        final = self.convert_geodf(final)

        final.to_file(self.fname)

        return final

    def __call__(self):

        return self.pipeline()

    

    

