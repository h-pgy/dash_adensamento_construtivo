from .read_iptu import IptuCsvReader
from .read_shapes import ReadShape

iptu_gen = IptuCsvReader()

read_shp_setores= ReadShape('setores_fiscais')
read_shp_quadras = ReadShape('quadras_fiscais')