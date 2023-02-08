import pandas as pd
import os

from core.utils.file_path import solve_path
from .transform_iptu import TransformAllIptu
from core.read_data import read_shp_quadras, read_shp_setores
from config import GENERATED_DATA_FOLDER
import geopandas as gpd

class JoinShp:


    def __init__(self, tipo:str)->None:


        self.tipo = tipo
        self.get_setores_iptu = TransformAllIptu(tipo=self.tipo)
        self.fname = solve_path(f'{self.tipo}_geodataframe.shp', GENERATED_DATA_FOLDER)

    def pivot_iptu(self, df:pd.DataFrame)->pd.DataFrame:

        pivotado = df.pivot(index=self.tipo, columns='ano', 
                                            values=[
                                                'sum_area_construida', 
                                                'mean_valor_do_m2_do_terreno',
                                                'mean_quantidade_de_pavimentos'
                                                ]
                                            )
        pivotado = pivotado.reset_index()
        pivotado.rename({'' : self.tipo},axis=1, inplace=True)

        return pivotado

    def solve_pivoted_column(self, df:pd.DataFrame)->pd.DataFrame:

        dfs = []
        for index in ['sum_area_construida', 'mean_valor_do_m2_do_terreno', 'mean_quantidade_de_pavimentos']:
            tmp = df[index]
            rename = {ano : f'{index}_{ano}' for 
                    ano in tmp.columns}
            tmp.rename(rename, axis=1, inplace=True)
            dfs.append(tmp)

        dfs.append(df[self.tipo])
        df = pd.concat(dfs, axis=1, ignore_index=False)

        return df

    def get_shape(self)->gpd.GeoDataFrame:

        if self.tipo == 'setor':
            shp = read_shp_setores()
        else:
            shp = read_shp_quadras()
        return shp

    def create_iptu_col(self, shp:gpd.GeoDataFrame)->None:

        if self.tipo=='setor':
            shp['setor'] = shp['st_codigo']
        else:
            shp['quadra'] = shp['qd_setor']+shp['qd_fiscal']
    
    def select_cols_shp(self, shp:gpd.GeoDataFrame)->gpd.GeoDataFrame:

        if self.tipo=='setor':
            return shp[['setor', 'geometry']]
        return shp[['quadra', 'geometry']]

    def merge(self, shp:gpd.GeoDataFrame, iptu:pd.DataFrame)->pd.DataFrame:

        final = pd.merge(shp, iptu, how='left').fillna(0)
        
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
        setores_iptu = self.pivot_iptu(setores_iptu) 
        setores_iptu = self.solve_pivoted_column(setores_iptu)
        shp_setores = self.get_shape()
        self.create_iptu_col(shp_setores)
        shp_setores = self.select_cols_shp(shp_setores)
        final = self.merge(shp_setores, setores_iptu)
        final = self.convert_geodf(final)

        final.to_file(self.fname)

        return final

    def __call__(self):

        return self.pipeline()

    

    

