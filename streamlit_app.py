import streamlit as st
import pydeck as pdk


with st.sidebar:
    st.image('https://observasampa.prefeitura.sp.gov.br/assets/img/logo.png')
    text = """
    ## Dashboard Adensamento Construtivo
    ### Cidade de São Paulo - 1995 a 2022

    Este aplicativo, a partir da análise da base de dados do **IPTU** para os anos de 1995 a 2022, permite visualizar o adensamento construtivo da cidade de São Paulo neste período.
    """
    st.markdown(text)

    st.markdown('#### **Desenvolvido por**: Henrique Pougy')
    col1, col2 = st.columns([0.5, 3])

    with col1:
        st.image('https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg', use_column_width=True)
    with col2:
        st.markdown('[linkedin](https://www.linkedin.com/in/henrique-pougy-8a008759?originalSubdomain=br)')

st.title('Adensamento Construtivo na Cidade de São Paulo', anchor=None)

ano = st.select_slider("Selecione o ano:", list(range(1995, 2023)))

def gerar_mapa_setores(col_altura = 'sum_area_construida', col_cor='sum_area_construida', 
                        ano=2022, dividir_altura = 1000):

    #tem que atualizar o link do ngrok
    data = 'https://raw.githubusercontent.com/h-pgy/dash_adensamento_construtivo/main/dados_setores.geojson'

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
        get_fill_color=f"[255, 255, 255]",
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

r = gerar_mapa_setores(ano=ano, dividir_altura=1000)

st.pydeck_chart(
    r
)