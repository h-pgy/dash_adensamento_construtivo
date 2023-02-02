import streamlit as st
import geopandas as gpd
import numpy as np
import pydeck as pdk
import json

with open('dados.geo_json', 'r') as f:
    dados = json.load(f)

geojson = pdk.Layer(
        "GeoJsonLayer",
        dados,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        get_elevation="sum_area_construida",
        #get_fill_color="[230, 230, (is_ZEU+1)*10]",
        get_line_color=[230, 230, 255],
        auto_highlight=True,

    )

view_state = pdk.ViewState(
    **{"latitude": -23.6, "longitude": -46.6, "zoom": 10, "maxZoom": 16, "pitch": 45, "bearing": 8}
)

r = pdk.Deck(
    [geojson],
    initial_view_state=view_state,
    map_style=pdk.map_styles.DARK,
)

st.pydeck_chart(
    r
)