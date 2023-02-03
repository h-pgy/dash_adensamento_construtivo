from config import IPTU_DATA_FOLDER, IPTU_YEARS

from ..utils.io import download_binary_file, unzip_file
from ..utils.file_path import solve_path, delete_existing_files, list_files


class IptuDownloader:

    domain = 'http://download.geosampa.prefeitura.sp.gov.br/'
    iptu_folder = IPTU_DATA_FOLDER
    iptu_years = IPTU_YEARS

    def solve_iptu_file_param(self, year:int)->None:

        return f'12_Cadastro%5C%5CIPTU_INTER%5C%5CXLS_CSV%5C%5CIPTU_{year}'

    def get_iptu_filename(self, year:int, extension:str)->str:

        assert extension in {'.zip', '.csv'}
        fname = f'{year}.{extension}'
        return solve_path(fname, parent=self.iptu_folder)
       
    def solve_uri(self, year:int)->str:

        fname = self.solve_iptu_file_param(year)
        endpoint = f'PaginasPublicas/downloadArquivo.aspx?orig=DownloadCamadas&arq={fname}&arqTipo=XLS_CSV'

        return self.domain + endpoint

    
    def download_iptu_file(self, year:int, save_file:str)->None:

        url = self.solve_uri(year)
        download_binary_file(url, save_file)

    def check_iptu_file_exists(self, year:int)->bool:

        files = list_files(self.iptu_folder)
        csv = [f for f in files if f.lower().endswith(f'{year}.csv')]

        return len(csv)>0

    def download_iptu_pipeline(self, year:int)->None:

        if self.check_iptu_file_exists(year):
            print(f'Arquivo {year}.csv ja salvo.')
            return

        zip_file = self.get_iptu_filename(year, extension='.zip')
        print(f'Downloading IPTU data for year {year}.')
        self.download_iptu_file(year, zip_file)
        unzip_file(zip_file, self.iptu_folder)
    
    def download_all_iptu(self, years:list=None, delete_zipfiles:bool=True)->None:

        years = years or self.iptu_years
        for year in years:
            self.download_iptu_pipeline(year)
        if delete_zipfiles:
            delete_existing_files(self.iptu_folder, extension='.zip')

    def __call__(self)->None:

        self.download_all_iptu()