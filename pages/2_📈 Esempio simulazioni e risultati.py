import streamlit as st
import pandas as pd
import plotly.express as px
import os
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

def plot_1(df, title_1, title_2, legend_title_1, legend_title_2, y_min, y_max_1, y_max_2, name):

    mask = ((df['Battery Rebate'] == battery_rebate) &
            (df['EC scenario'] == ec_scenario) &
            (df['FiT'] == fit) &
            (df['PV Rebate'] == pv_rebate) &
            (df['Share PV Cantonal over Federal rebate'] == share_pv))
    filtered = df[mask]

    df1 = filtered[filtered['Type'].isin(res_types)]
    df2 = filtered[filtered['Type'].isin(['< 100 kW', '> 100 kW'])]

    df_melt = df1.melt(id_vars=['Type'],
                       value_vars=year_cols,
                       var_name='Anno',
                       value_name=name)

    fig1 = px.line(
        df_melt, x='Anno', y=name, color='Type', markers=True, title=title_1,
        labels={'Type': legend_title_1}
    )
    fig1.update_layout(
        title=dict(text=title_1, x=0.5, xanchor="center", y=0.85),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)')
    )
    fig1.update_yaxes(range=[y_min, y_max_1])

    df_melt = df2.melt(id_vars=['Type'],
                       value_vars=year_cols,
                       var_name='Anno',
                       value_name=name)

    df_melt['Anno'] = df_melt['Anno'].astype(int)
    fig2 = px.line(
        df_melt, x='Anno', y=name, color='Type', markers=True, title=title_2,
        labels={'Type': legend_title_2}
    )
    fig2.update_layout(
        title=dict(text=title_2, x=0.5, xanchor="center", y=0.85),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)')
    )
    fig2.update_yaxes(range=[y_min, y_max_2])

    return fig1, fig2


def plot_comparison(df, title, y_max, value_name):

    mask_current = (
        (df['Battery Rebate'] == battery_rebate) &
        (df['EC scenario'] == ec_scenario) &
        (df['FiT'] == fit) &
        (df['PV Rebate'] == pv_rebate) &
        (df['Share PV Cantonal over Federal rebate'] == share_pv)
    )
    df_current = df[mask_current]

    mask_baseline = (
        (df['Battery Rebate'] == 0) &
        (df['EC scenario'] == 0) &
        (df['FiT'] == 0) &
        (df['PV Rebate'] == 0.2) &
        (df['Share PV Cantonal over Federal rebate'] == 0.5)
    )
    df_baseline = df[mask_baseline]

    categories = res_types + ['< 100 kW', '> 100 kW']

    df_current = df_current[df_current['Type'].isin(categories)][['Type', str(2050)]].copy()
    df_baseline = df_baseline[df_baseline['Type'].isin(categories)][['Type', str(2050)]].copy()

    df_compare = pd.merge(df_current, df_baseline, on="Type", suffixes=('_Current', '_Baseline'))

    df_melt = df_compare.melt(id_vars="Type", value_vars=[f"{2050}_Current", f"{2050}_Baseline"],
                              var_name="Scenario", value_name=value_name)

    df_melt["Scenario"] = df_melt["Scenario"].replace({
        f"{2050}_Current": "Scenario selezionato",
        f"{2050}_Baseline": "Scenario BAU"
    })

    fig = px.bar(
        df_melt, x="Type", y=value_name, color="Scenario",
        barmode="group", text_auto=True
    )
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", y=0.85),
        legend=dict(x=0.25, y=0.9, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)')
    )
    fig.update_yaxes(range=[0, y_max])
    return fig


def plot_2(df, title, y_max):
    mask_current = (
            (df['Battery Rebate'] == battery_rebate) &
            (df['EC scenario'] == ec_scenario) &
            (df['FiT'] == fit) &
            (df['PV Rebate'] == pv_rebate) &
            (df['Share PV Cantonal over Federal rebate'] == share_pv)
    )
    df_mask_current = df[mask_current]

    mask_baseline = (
            (df['Battery Rebate'] == 0) &
            (df['EC scenario'] == 0) &
            (df['FiT'] == 0) &
            (df['PV Rebate'] == 0.2) &
            (df['Share PV Cantonal over Federal rebate'] == 0.5)
    )
    df_mask_baseline = df[mask_baseline]

    categories = res_types

    df_current = df_mask_current[df_mask_current['Type'].isin(categories)][['Type', str(2050)]].copy()
    df_baseline = df_mask_baseline[df_mask_baseline['Type'].isin(categories)][['Type', str(2050)]].copy()

    df_compare = pd.merge(df_current, df_baseline, on="Type", suffixes=('_Current', '_Baseline'))

    df_melt = df_compare.melt(id_vars="Type", value_vars=[f"{2050}_Current", f"{2050}_Baseline"],
                              var_name="Scenario", value_name="[-]")

    df_melt["Scenario"] = df_melt["Scenario"].replace({
        f"{2050}_Current": "Scenario selezionato",
        f"{2050}_Baseline": "Scenario BAU"
    })

    fig = px.bar(
        df_melt, x="Type", y="[-]", color="Scenario",
        barmode="group", text_auto=True,
        title=title
    )
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", y=0.9),
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)'),
        yaxis_title="[-]",
        xaxis_title=None
    )
    fig.update_yaxes(range=[0, y_max])

    return fig, df_mask_current, df_mask_baseline


def plot_3(df, title, legend_title, y_max, y_legend, value_name):
    mask = ((df['Battery Rebate'] == battery_rebate) &
            (df['EC scenario'] == ec_scenario) &
            (df['FiT'] == fit) &
            (df['PV Rebate'] == pv_rebate) &
            (df['Share PV Cantonal over Federal rebate'] == share_pv))
    filtered = df[mask]

    df_melt = filtered.melt(id_vars=['Type'], value_vars=year_cols, var_name='Anno', value_name=value_name)
    df_melt['Anno'] = df_melt['Anno'].astype(int)

    fig = px.line(
        df_melt,
        x='Anno',
        y=value_name,
        color='Type',
        markers=True,
        title=title,
        labels={'Type': legend_title}
    )
    fig.update_layout(
        legend=dict(x=0, y=y_legend, xanchor='left', yanchor='middle', bgcolor='rgba(255,255,255,0.7)'),
        title=dict(text=title, x=0.5, xanchor="center", y=0.9)
    )
    fig.update_yaxes(range=[0, y_max])

    return fig


def plot_4(df, title, y_min, y_max):
    mask_current = (
            (df['Battery Rebate'] == battery_rebate) &
            (df['EC scenario'] == ec_scenario) &
            (df['FiT'] == fit) &
            (df['PV Rebate'] == pv_rebate) &
            (df['Share PV Cantonal over Federal rebate'] == share_pv)
    )
    df_current = df[mask_current].copy()
    df_current = df_current.melt(
        id_vars=['Type'],
        value_vars=['Domanda', 'Produzione PV', 'Autoconsumo'],
        var_name='Categoria',
        value_name='[GWh]'
    )
    df_current['Scenario'] = "Scenario selezionato"

    # --- Baseline scenario ---
    mask_baseline = (
            (df['Battery Rebate'] == 0) &
            (df['EC scenario'] == 0) &
            (df['FiT'] == 0) &
            (df['PV Rebate'] == 0.2) &
            (df['Share PV Cantonal over Federal rebate'] == 0.5)
    )
    df_baseline = df[mask_baseline].copy()
    df_baseline = df_baseline.melt(
        id_vars=['Type'],
        value_vars=['Domanda', 'Produzione PV', 'Autoconsumo'],
        var_name='Categoria',
        value_name='[GWh]'
    )
    df_baseline['Scenario'] = "Scenario BAU"

    # --- Combine current + baseline ---
    df_all = pd.concat([df_current, df_baseline], axis=0)

    df_all["scenario"] = df_all["Categoria"] + " - " + df_all["Scenario"]

    fig = px.bar(df_all,
                 x='Type',
                 y='[GWh]',
                 color='scenario',
                 barmode='group'
                 )

    fig.update_layout(
        legend=dict(x=1, y=1, xanchor='right', yanchor='top', bgcolor='rgba(255,255,255,0.7)'),
        title=dict(text=title, x=0.5, xanchor="center", y=0.9),
        xaxis_title=None
    )
    fig.update_yaxes(range=[y_min, y_max])

    return fig


def plot_5(df, title, legend_title, y_min=0, y_max=0.4):
    mask = ((df['Battery Rebate'] == battery_rebate) &
            (df['EC scenario'] == ec_scenario) &
            (df['FiT'] == fit) &
            (df['PV Rebate'] == pv_rebate) &
            (df['Share PV Cantonal over Federal rebate'] == share_pv))
    filtered = df[mask]

    df_melt = filtered.melt(id_vars=['Type'], value_vars=year_cols, var_name='Anno', value_name='[CHF/kWh]')
    df_melt['Anno'] = df_melt['Anno'].astype(int)
    fig = px.line(
        df_melt,
        x='Anno',
        y='[CHF/kWh]',
        color='Type',
        markers=True,
        title=title,
        labels={'Type': legend_title}
    )
    fig.update_layout(
        legend=dict(x=0, y=0.25, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)', title=None, orientation="h"),
        title=dict(text=title, x=0.5, xanchor="center", y=0.9)
    )
    fig.update_yaxes(range=[y_min, y_max])
    return fig


# Slider nella sidebar

st.sidebar.markdown("<h2>Parametri di input</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<h7>Incentivi federali</h7>", unsafe_allow_html=True)

pv_rebate = st.sidebar.slider("Incentivo FV", 0.0, 0.4, 0.0, 0.1,
                              help='Frazione del costo di investimento coperta (attualmente circa 0.2).',
                              key="pv_rebate")

st.sidebar.markdown("<h7>Incentivi cantonali</h7>", unsafe_allow_html=True)

fit = st.sidebar.slider("Tariffa di ritiro [CHF/kWh]", 0.0, 0.1, 0.0, 0.025,
                        format="%.3f",
                        help='Rimunerazione per l\'elettricità immessa in rete in aggiunta al prezzo di mercato di '
                             'riferimento (attualmente pari a 0).',
                        key="fit_slider")
share_pv = st.sidebar.slider("Quota incentivo cantonale su federale", 0.0, 0.5, 0.0, 0.1,
                             help='Frazione dell\'incentivo federale che il Cantone aggiunge (attualmente pari a 0.5).',
                             key="share_pv")
battery_rebate = st.sidebar.slider("Incentivo batterie", 0.0, 0.3, 0.0, 0.1,
                                   help='Frazione del costo di investimento coperta (attualmente pari a 0).',
                                   key="battery_rebate")
ec_scenario = st.sidebar.radio("Possibilità creazione RCPv", [0, 1], index=0,
                               format_func=lambda x: "No" if x == 0 else "Sì",
                               key="ec_scenario")

results_path = os.path.dirname(os.path.dirname(__file__))

year_cols = [str(y) for y in range(2011, 2051)]
res_types = ['SFH', 'DFH', 'MFH']


# 1. Diffusione energia fotovoltaica

@st.cache_data
def data1(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    df = df.round(2)
    return df

df = data1('/plots_data/Power installed.csv')
[fig1, fig2] = plot_1(df, "Potenza installata in edifici residenziali", "Potenza installata in edifici non residenziali", "Tipo di edificio residenziale", "Taglia dell'impianto", 0, 600, 600, 'Potenza installata [MW]')
fig20 = plot_comparison(df, "Potenza installata nel 2050", 600, 'Potenza installata [MW]')

@st.cache_data
def data2(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    df = df.round(3)
    return df

df = data2('/plots_data/Share buildings PV.csv')
[fig_bar1, df_current, df_baseline] = plot_2(df, "Frazione di edifici residenziali <br> con un impianto nel 2050", 1)


@st.cache_data
def upload_district_geometries(file_name):

    gdf_district = gpd.read_file(results_path + file_name, columns=['NAME', 'KANTONSNUM', 'geometry'], engine='pyogrio')
    if gdf_district.crs != "EPSG:4326":
        gdf_district = gdf_district.to_crs(epsg=4326)
    gdf_district = gdf_district.loc[gdf_district['KANTONSNUM'] == 21]

    return gdf_district

gdf_district = upload_district_geometries('/Limits/swissBOUNDARIES3D_1_4_TLM_BEZIRKSGEBIET.shp')

df_dist_current = df_current[~df_current['Type'].isin(res_types)]
gdf_map_current = gdf_district.merge(df_dist_current, left_on='NAME', right_on='Type', how='inner')
gdf_map_current = gdf_map_current.dropna(subset=['2050'])
gdf_map_current = gdf_map_current.to_crs(epsg=4326)

colormap = cm.linear.YlOrRd_09.scale(0.2, 0.9)
center = gdf_map_current.geometry.union_all().centroid
m1_current = folium.Map(location=[center.y, center.x], zoom_start=8, tiles='CartoDB positron')

folium.GeoJson(
    gdf_map_current,
    style_function=lambda feature: {
        'fillColor': colormap(feature['properties']['2050']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['NAME', '2050'], aliases=['Distretto:', 'Share PV 2050:'], localize=True)
).add_to(m1_current)

df_dist_baseline = df_baseline[~df_baseline['Type'].isin(res_types)]
gdf_map_baseline = gdf_district.merge(df_dist_baseline, left_on='NAME', right_on='Type', how='inner')
gdf_map_baseline = gdf_map_baseline.dropna(subset=['2050'])
gdf_map_baseline = gdf_map_baseline.to_crs(epsg=4326)

m1_baseline = folium.Map(location=[center.y, center.x], zoom_start=8, tiles='CartoDB positron')

folium.GeoJson(
    gdf_map_baseline,
    style_function=lambda feature: {
        'fillColor': colormap(feature['properties']['2050']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['NAME', '2050'], aliases=['Distretto:', 'Share PV 2050:'], localize=True)
).add_to(m1_baseline)

# 2. Adozione batterie

@st.cache_data
def data3(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    df = df.round(3)
    return df

df = data3('/plots_data/Battery installed capacity.csv')
[fig3, fig4] = plot_1(df, "Capacità installata in edifici residenziali", "Capacità installata in edifici non residenziali", "Tipo di edificio residenziale", "Taglia dell'impianto", 0, 300, 60, 'Capacità installata [MWh]')
fig21 = plot_comparison(df, "Potenza installata nel 2050", 300, 'Capacità installata [MWh]')


@st.cache_data
def data4(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    df = df.round(2)
    return df

df = data4('/plots_data/Share buildings battery.csv')
[fig_bar2, df_current, df_baseline] = plot_2(df, "Frazione di edifici con PV che <br> hanno anche una batteria nel 2050", 1)

df_dist_current = df_current[~df_current['Type'].isin(res_types)]
gdf_map_current = gdf_district.merge(df_dist_current, left_on='NAME', right_on='Type', how='inner')
gdf_map_current = gdf_map_current.dropna(subset=['2050'])
gdf_map_current = gdf_map_current.to_crs(epsg=4326)

colormap2 = cm.linear.YlOrRd_09.scale(0, 220)
m2_current = folium.Map(location=[center.y, center.x], zoom_start=8, tiles='CartoDB positron')

folium.GeoJson(
    gdf_map_current,
    style_function=lambda feature: {
        'fillColor': colormap2(feature['properties']['2050']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['NAME', '2050'], aliases=['Distretto:', 'Capacità [MWh]:'], localize=True)
).add_to(m2_current)

df_dist_baseline = df_baseline[~df_baseline['Type'].isin(res_types)]
gdf_map_baseline = gdf_district.merge(df_dist_baseline, left_on='NAME', right_on='Type', how='inner')
gdf_map_baseline = gdf_map_baseline.dropna(subset=['2050'])
gdf_map_baseline = gdf_map_baseline.to_crs(epsg=4326)

m2_baseline = folium.Map(location=[center.y, center.x], zoom_start=8, tiles='CartoDB positron')

folium.GeoJson(
    gdf_map_baseline,
    style_function=lambda feature: {
        'fillColor': colormap2(feature['properties']['2050']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['NAME', '2050'], aliases=['Distretto:', 'Capacità [MWh]:'], localize=True)
).add_to(m2_baseline)


# 3. Domanda elettricità e produzione PV

@st.cache_data
def data5(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    df = df.round(2)
    return df

df = data5('/plots_data/Electricity produced and consumed.csv')
fig5 = plot_3(df, "Evoluzione della domanda, produzione e <br>autoconsumo PV (Ticino)", "", 3500, 0.5, value_name='Cantone [GWh]')


@st.cache_data
def data6(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    df = df.round(2)
    return df

df = data6('/plots_data/Electricity produced and consumed District.csv')
fig_bar3 = plot_4(df, "Domanda, produzione e autoconsumo PV nel 2050 per distretto", 0, 1000)


# 4. Prezzo dell'elettricità e ripartizione dei costi

@st.cache_data
def data7(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    return df

df = data7('/plots_data/Cost federal Levy.csv')
fig9 = plot_3(df, "Costo annuale per supplemento rete federale per un'unità familare <br> media in base al tipo di edificio e al possesso di PV", "", 400, 0.9, value_name='[CHF]')


@st.cache_data
def data8(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    return df

df = data8('/plots_data/Cost cantonal Levy.csv')
fig10 = plot_3(df, "Costo annuale per supplemento rete cantonale per un'unità familare <br> media in base al tipo di edificio e al possesso di PV", "", 400, 0.9, value_name='[CHF]')


@st.cache_data
def data7(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    return df

df = data7('/plots_data/Electricity price.csv')
fig6 = plot_5(df, "Prezzo elettricità", "", 0, 0.5)


@st.cache_data
def data8(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    return df

df = data8('/plots_data/Levy.csv')
fig7 = plot_3(df, "Supplemento rete per <br> finanziamento incentivi", "", 0.1, 0.9, value_name='[CHF/kWh]')


@st.cache_data
def data9(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    return df

df = data9('/plots_data/Grid updating cost.csv')
fig8 = plot_3(df, "Costo annuale rinforzo rete", "", 40, 0.9, value_name='[Mio CHF]')


# Layout della pagina

st.set_page_config(page_title="Esempio simulazioni e risultati", page_icon="📈", layout="wide")

st.title("📈 Esempio simulazioni e risultati")

st.markdown(
    """
    In questa pagina è riportato un esempio di utilizzo del modello di transizione cantonale. 
    Come si vede nell'immagine sottostante, questo esempio si concentra sulla diffusione di:
    
    - 🌞 **Pannelli fotovoltaici**  
    - 🔋 **Batterie decentralizzate**
    - 💡 **Raggruppamenti per Consumo Proprio**  
    
    Sulla sinistra si possono modificare interattivamente gli input che rappresentano decisioni politiche riguardanti 
    queste tecnologie. In basso si possoono selezionare i risultati da visualizzare in base alle proprie preferenze.

    ---
    """
)


st.image(results_path + "/images/Image.png", caption="")

st.markdown("### Seleziona i risultati da visualizzare")
selections = st.multiselect(
    "Scegli la sezione:",
    [
        "Diffusione energia fotovoltaica",
        "Adozione batterie",
        "Domanda elettricità e produzione PV",
        "Prezzo dell'elettricità e ripartizione dei costi"
    ]
)



if "Diffusione energia fotovoltaica" in selections:
    st.subheader("Diffusione energia fotovoltaica")
    row1, row2, row3 = st.columns([1, 1, 1])
    with row1:
        st.plotly_chart(fig1.update_layout(height=450), use_container_width=True)
    with row2:
        st.plotly_chart(fig2.update_layout(height=450), use_container_width=True)
    with row3:
        st.plotly_chart(fig20.update_layout(height=450), use_container_width=True)

    row1, row2 = st.columns([1, 2])
    with row1:
        st.plotly_chart(fig_bar1.update_layout(height=400), use_container_width=True)
    with row2:
        st.markdown(
            """
            **Frazione di edifici residenziali con PV nel 2050 - Scenario selezionato (sx) vs Scenario 
            BAU (dx)**
            """
        )
        row3, row4 = st.columns([1, 1])
        with row3:
            st_folium(m1_current, key="map_current", width=None, height=350)
        with row4:
            st_folium(m1_baseline, key="map_baseline", width=None, height=350)

if "Adozione batterie" in selections:
    st.subheader("Adozione batterie")
    row1, row2, row3 = st.columns([1, 1, 1])
    with row1:
        st.plotly_chart(fig3.update_layout(height=450), use_container_width=True)
    with row2:
        st.plotly_chart(fig4.update_layout(height=450), use_container_width=True)
    with row3:
        st.plotly_chart(fig21.update_layout(height=450), use_container_width=True)

    row1, row2 = st.columns([1, 2])
    with row1:
        st.plotly_chart(fig_bar2.update_layout(height=400), use_container_width=True)
    with row2:
        st.markdown(
            """
            **Totale capacità batterie installata nel 2050 - Scenario selezionato 
            (sx) vs Scenario BAU (dx)**
            """
        )
        row3, row4 = st.columns([1, 1])
        with row3:
            st_folium(m2_current, key="map_battery_current", width=None, height=350)
        with row4:
            st_folium(m2_baseline, key="map_battery_baseline", width=None, height=350)

if "Domanda elettricità e produzione PV" in selections:
    st.subheader("Domanda elettricità e produzione PV")
    row1, row2 = st.columns([1, 2])
    with row1:
        st.plotly_chart(fig5.update_layout(height=400), use_container_width=True)
    with row2:
        st.plotly_chart(fig_bar3.update_layout(height=400), use_container_width=True)

if "Prezzo dell'elettricità e ripartizione dei costi" in selections:
    st.subheader("Prezzo dell'elettricità e ripartizione dei costi")
    row1, row2, row3 = st.columns([1.7, 1, 1])
    with row1:
        st.plotly_chart(fig6.update_layout(height=350), use_container_width=True)
    with row2:
        st.plotly_chart(fig7.update_layout(height=350), use_container_width=True)
    with row3:
        st.plotly_chart(fig8.update_layout(height=350), use_container_width=True)

    row1, row2 = st.columns(2)
    with row1:
        st.plotly_chart(fig9, use_container_width=True)
    with row2:
        st.plotly_chart(fig10, use_container_width=True)