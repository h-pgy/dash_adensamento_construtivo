import streamlit as st
import pydeck as pdk
import json
from copy import copy
import requests
from core.transform_data import shp_setores_calculado

st.title('Adensamento Construtivo da Cidade de São Paulo', anchor=None)

def gerar_mapa_setores(col_altura = 'sum_area_construida', ano=2022, dividir_altura = 1000):
    
    data = 'https://raw.githubusercontent.com/h-pgy/dash_adensamento_construtivo/main/data.geojson'
    layer = pdk.Layer(
        "GeoJsonLayer",
        data,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        get_elevation =f"properties.{col_altura}_{ano}/{dividir_altura}",
        get_fill_color=f"[0.0000255*properties.{col_altura}_{ano}, 100, 0]",
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