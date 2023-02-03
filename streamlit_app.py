import streamlit as st
import pydeck as pdk
import json
from copy import copy
import requests

st.title('Adensamento Construtivo da Cidade de São Paulo', anchor=None)

@st.cache(allow_output_mutation=True)
def filtrar_ano_geojson(geojson:dict, ano:int)->dict:
    
    filtered = []
    geojson = copy(geojson)
    for f in geojson['features']:
        if f['properties']['ano']==ano:
            filtered.append(f)
            
    geojson['features']=filtered
    
    return geojson

def gerar_mapa_setores(col_altura = 'sum_area_c', dividir_altura = 1000):
    
    data = 'https://raw.githubusercontent.com/h-pgy/dash_adensamento_construtivo/main/dados.geojson'
    layer = pdk.Layer(
        "GeoJsonLayer",
        data,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        get_elevation =f"properties.{col_altura}/{dividir_altura}",
        get_fill_color="[255, 255, properties.mean_valor*255]",
        get_line_color=[230, 230, 255],
        auto_highlight=True,

    )

    view_state = pdk.ViewState(
        **{"latitude": -23.6, "longitude": -46.6, "zoom": 10, "maxZoom": 16, "pitch": 45, "bearing": 8}
    )
    
    r = pdk.Deck(
        layer,
        initial_view_state=view_state,
        map_style=pdk.map_styles.DARK,
    )
    
    return r

r = gerar_mapa_setores()

st.pydeck_chart(
    r
)