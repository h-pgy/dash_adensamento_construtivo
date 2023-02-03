import geopandas as gpd
from config import SHP_FOLDER
from core.utils.file_path import list_files_recursive, solve_path

class ReadShape:

    def __init__(self, alias:str)->None:

        self.alias = alias
        self.folder = self.get_folder()
        

    def get_folder(self)->str:

        shp_folder = solve_path(self.alias, SHP_FOLDER)

        return shp_folder

    def get_shape_fpath(self)->str:

        return list_files_recursive(self.folder, 'shp')[0]

    def read_shape(self, fpath)->gpd.GeoDataFrame:

        return gpd.read_file(fpath)

    def __call__(self)->gpd.GeoDataFrame:

        shp_path = self.get_shape_fpath()

        return self.read_shape(shp_path)