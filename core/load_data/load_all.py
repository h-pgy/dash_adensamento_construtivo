from .geosampa import ShpDownloader
from .iptu import IptuDownloader


def load_all():

    geosampa = ShpDownloader()
    iptu = IptuDownloader()

    geosampa()
    iptu()