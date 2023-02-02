import geopandas as gpd
from config import SHP_FOLDER
from core.utils.file_path import list_files_recursive, solve_path

class ReadQuadras:

    def __init__(self):

        self.folder = self.get_folder()

    def get_folder(self):

        quadras_shp_folder = solve_path('quadras_fiscais', SHP_FOLDER)

        return quadras_shp_folder

    def get_shape_fpath(self):

        return list_files_recursive(self.folder, 'shp')[0]

    def read_shape(self, fpath):

        return gpd.read_file(fpath)

    def __call__(self):

        shp_path = self.get_shape_fpath()

        return self.read_shape(shp_path)