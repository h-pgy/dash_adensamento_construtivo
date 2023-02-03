import pandas as pd
from typing import List

class GroupbySetor:
    """Limpa os dados e os agrupa por setores"""
    
    cols_numericas = {
        'AREA CONSTRUIDA' : 'soma',
        'VALOR DO M2 DO TERRENO' : 'media',
        'QUANTIDADE DE PAVIMENTOS' : 'media'
        }
    
    def extract_ano(self, df:pd.DataFrame)->int:
        
        return df['ano_arquivo'].unique()[0]
    
    def extract_setores(self, df:pd.DataFrame)->None:
    
        contrib_col = 'NUMERO DO CONTRIBUINTE'
        df['setor'] = df[contrib_col].str.slice(0, 3)
    
    def col_to_numeric(self, df:pd.DataFrame,col:str)->None:
        
        if df[col].dtype == 'O':
            df[col] = df[col].str.replace(',', '.')
            
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    def cols_to_numeric(self, df:pd.DataFrame)->None:
    
        for col in self.cols_numericas:
            self.col_to_numeric(df, col)
            
    def groupby_setor(self, df:pd.DataFrame)->pd.DataFrame:
        
        grouped = df.groupby('setor')
        
        return grouped
    
    @property
    def cols_media(self)->List[str]:
        
        cols_media = [col for col, acao in self.cols_numericas.items()
                          if acao == 'media']
        
        return cols_media
    
    @property
    def cols_sum(self)->List[str]:
        
        cols_sum = [col for col, acao in self.cols_numericas.items()
                          if acao == 'soma']
        
        return cols_sum
    
    def rename_cols(self, df:pd.DataFrame, operacao:str)->None:
        
        cols = df.columns
        
        df.rename({col : f'{operacao}_{col.lower().replace(" ", "_")}'
                 for col in cols}, axis = 1, inplace=True)
        
    
    def grouped_media(self, grouped:pd.DataFrame, ano:int)->pd.DataFrame:
        
        medias = grouped[self.cols_media].mean()
        self.rename_cols(medias, 'mean')
        medias['ano'] = ano
        
        return medias.reset_index()
    
    def grouped_soma(self, grouped:pd.DataFrame, ano:int)->pd.DataFrame:
        
        somas = grouped[self.cols_sum].sum()
        self.rename_cols(somas, 'sum')
        somas['ano'] = ano
        
        return somas.reset_index()
    
    def join_grouped(self, somas:pd.DataFrame, medias:pd.DataFrame)->pd.DataFrame:
        
        return pd.merge(somas, medias, on='setor', how='inner')
    
    def pipeline(self, df:pd.DataFrame)->pd.DataFrame:
        
        self.extract_setores(df)
        self.cols_to_numeric(df)
        
        ano = self.extract_ano(df)
        grouped = self.groupby_setor(df)
        
        medias = self.grouped_media(grouped, ano)
        somas = self.grouped_soma(grouped, ano)
        
        joined = self.join_grouped(somas, medias)
        
        return joined
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:
        
        return self.pipeline(df)