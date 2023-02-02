
from core.utils.file_path import solve_dir, solve_path

ORIGINAL_DATA_FOLDER = solve_dir('original_data')
SHP_FOLDER = solve_dir(solve_path('shp_files', ORIGINAL_DATA_FOLDER))
ZIP_FOLDER = solve_dir(solve_path('shp_zips', ORIGINAL_DATA_FOLDER))
IPTU_DATA_FOLDER = solve_dir(solve_path('iptu_data', ORIGINAL_DATA_FOLDER))

GENERATED_DATA_FOLDER = 'data'

URIS_CAMADAS = {
    #'quadras_fiscais' : r'12_Cadastro%5C%5CQuadra%5C%5CShapefile%5C%5CSIRGAS_SHP_quadraMDSF',
    'quadras_fiscais' : r'12_Cadastro\\Setor\\Shapefile\\SIRGAS_SHP_setorfiscal',
    'zoneamento' : r'13_Legisla%E7%E3o%20Urbana%5C%5CZoneamento_Lei16402-16_Mapa_01_Principal%5C%5CShapefile%5C%5CMapa-1-SHP',
}

IPTU_YEARS = range(2013, 2023)