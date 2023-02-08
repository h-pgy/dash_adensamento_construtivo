import streamlit as st
import pydeck as pdk
import json
from copy import copy
import requests
import requests
import time

st.title('Adensamento Construtivo da Cidade de São Paulo', anchor=None)

ano = st.selectbox(
    'Escolha o ano?',
    ('1995', '2013', '2022'))

def gerar_mapa_setores(col_altura = 'prop_area_construida', col_cor='prop_area_construida', 
                        ano=2022, dividir_altura = 1000):

    #tem que atualizar o link do ngrok
    ngrok = 'https://5239-2804-7f0-bcc0-af09-53b1-4844-a929-ae44.sa.ngrok.io'
    data = ngrok + '/data.geojson'
    

    col_altura = f'{col_altura}_{ano}'
    col_cor = f'{col_cor}_{ano}'
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
        get_fill_color=f"[255, 255/properties.{col_cor}, 0]",
        get_line_color=[230, 230, 255],
        auto_highlight=True,

    )

    view_state = pdk.ViewState(
        **{"latitude": -23.6, "longitude": -46.6, "zoom": 10, "maxZoom": 16, "pitch": 45, "bearing": 8}
    )

    tooltip = {
   "html": f"<b>Altura:</b> {{properties.{col_altura}}} <br/>",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
        }
    }
    
    r = pdk.Deck(
        layer,
        initial_view_state=view_state,
        map_style=pdk.map_styles.DARK,
        tooltip=tooltip
    )
    
    return r

r = gerar_mapa_setores(ano=ano, dividir_altura=0.001)

st.pydeck_chart(
    r
)