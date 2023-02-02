import pandas as pd

class GroupbyQuadra:
    """Limpa os dados e os agrupa por quadras"""
    
    cols_numericas = {
        'AREA CONSTRUIDA' : 'soma',
        'VALOR DO M2 DO TERRENO' : 'media',
        'QUANTIDADE DE PAVIMENTOS' : 'media'
        }
    
    def extract_ano(self, df):
        
        return df['ano_arquivo'].unique()[0]
    
    def extract_quadra(self, df):
    
        contrib_col = 'NUMERO DO CONTRIBUINTE'
        df['quadra'] = df[contrib_col].str.slice(0, -6)
    
    def col_to_numeric(self, df,col):
        
        if df[col].dtype == 'O':
            df[col] = df[col].str.replace(',', '.')
            
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    def cols_to_numeric(self, df):
    
        for col in self.cols_numericas:
            self.col_to_numeric(df, col)
            
    def groupby_quadra(self, df):
        
        grouped = df.groupby('quadra')
        
        return grouped
    
    @property
    def cols_media(self):
        
        cols_media = [col for col, acao in self.cols_numericas.items()
                          if acao == 'media']
        
        return cols_media
    
    @property
    def cols_sum(self):
        
        cols_sum = [col for col, acao in self.cols_numericas.items()
                          if acao == 'soma']
        
        return cols_sum
    
    def rename_cols(self, df, acao):
        
        cols = df.columns
        
        df.rename({col : f'{acao}_{col.lower().replace(" ", "_")}'
                 for col in cols}, axis = 1, inplace=True)
        
    
    def grouped_media(self, grouped, ano):
        
        medias = grouped[self.cols_media].mean()
        self.rename_cols(medias, 'mean')
        medias['ano'] = ano
        
        return medias.reset_index()
    
    def grouped_soma(self, grouped, ano):
        
        somas = grouped[self.cols_sum].sum()
        self.rename_cols(somas, 'sum')
        somas['ano'] = ano
        
        return somas.reset_index()
    
    def join_grouped(self, somas, medias):
        
        return pd.merge(somas, medias, on='quadra', how='inner')
    
    def pipeline(self, df):
        
        self.extract_quadra(df)
        self.cols_to_numeric(df)
        
        ano = self.extract_ano(df)
        grouped = self.groupby_quadra(df)
        
        medias = self.grouped_media(grouped, ano)
        somas = self.grouped_soma(grouped, ano)
        
        joined = self.join_grouped(somas, medias)
        
        return joined
    
    def __call__(self, df):
        
        return self.pipeline(df)