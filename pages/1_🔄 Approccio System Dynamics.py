import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
import geopandas as gpd
import time


def plot_pie(df, year):

    df_pie = df[df["year"] == year].drop(columns="year").T.reset_index()
    df_pie.columns = ["Settore", "Consumi"]
    fig = px.pie(
        df_pie,
        names="Settore",
        values="Consumi",
        title=None
    )
    fig.update_layout(showlegend=False)
    return fig


results_path = os.path.dirname(os.path.dirname(__file__))


with open(results_path + "/map.html", "r", encoding="utf-8") as f:
    map_html = f.read()

@st.cache_data
def upload_data_and_plot1(file_name, title):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')

    df_melt = df.melt(id_vars="year", var_name="Settore", value_name="[GWh]")
    fig = px.bar(
        df_melt,
        x="year",
        y="[GWh]",
        color="Settore",
        title=title,
        labels={"year": "Anno"}
    )
    fig.update_layout(
        legend=dict(x=0, y=1.3, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)', title=None, orientation="h"),
        title=dict(text=title, x=0.5, xanchor="center", y=1)
    )
    return df, fig
[df1, fig1] = upload_data_and_plot1('/plots_data/Historical energy consumption.csv', "Consumo energia annuale per settore")


@st.cache_data
def upload_data_and_plot2(file_name, title):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')

    df_melt = df.melt(id_vars="year", var_name="Settore", value_name="[GWh]")
    fig = px.bar(
        df_melt,
        x="year",
        y="[GWh]",
        color="Settore",
        title=title,
        labels={"year": "Anno"}
    )
    fig.update_layout(
        legend=dict(x=0, y=1.3, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)', title=None, orientation="h"),
        title=dict(text=title, x=0.5, xanchor="center", y=1)
    )
    return df, fig
[df2, fig2] = upload_data_and_plot2('/plots_data/Historical electricity consumption.csv', "Consumo elettricità annuale per settore")


@st.cache_data
def upload_data_and_plot3(file_name, title):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')

    df_melt = df.melt(id_vars="Year", var_name="Riscaldamento", value_name="Installazioni annue")
    df_melt['Year'] = df_melt['Year'].astype(int)
    fig = px.line(
        df_melt,
        x="Year",
        y="Installazioni annue",
        color="Riscaldamento",
        title=title,
        labels={"Year": "Anno"}
    )
    fig.update_layout(
        legend=dict(x=0, y=1, xanchor='left', yanchor='top', bgcolor='rgba(255,255,255,0.7)', title=None, orientation="h"),
        title=dict(text=title, x=0.5, xanchor="center", y=0.9)
    )
    fig.update_yaxes(range=[0, 3000])
    return fig
fig3 = upload_data_and_plot3('/plots_data/Annual adoption HT.csv', "Installazioni annue di nuovi sistemi<br>di riscaldamento (settore residenziale)")


@st.cache_data
def upload_data_HP(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')
    return df
df_HP = upload_data_HP('/plots_data/Annual adoption HP.csv')


@st.cache_data
def upload_data_and_plot4(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', on_bad_lines='skip')

    columns_1 = ["Idroelettrico", "Altro"]
    fig1 = px.line(df, x="year", y=columns_1, markers=True,
                  labels={"value": "[GWh]", "variable": "", "year": "Anno"})
    fig1.update_layout(
        legend=dict(x=0, y=0.9, xanchor='left', yanchor='middle', bgcolor='rgba(255,255,255,0.7)'),
        title=dict(text='Produzione totale annua', x=0.5, xanchor="center", y=0.95)
    )

    columns_2 = ['Fotovoltaico', 'Acqua fluente', 'Cogenerazione', 'Eolico']
    fig2 = px.line(df, x="year", y=columns_2, markers=True,
                   labels={"value": "[GWh]", "variable": "", "year": "Anno"})
    fig2.update_layout(
        legend=dict(x=0, y=0.9, xanchor='left', yanchor='middle', bgcolor='rgba(255,255,255,0.7)'),
        title=dict(text='Produzione totale annua', x=0.5, xanchor="center", y=0.95)
    )

    return fig1, fig2

[fig4, fig5] = upload_data_and_plot4('/plots_data/Historical electricity production.csv')


@st.cache_data
def upload_data_gdf(file_name):
    gdf_PV = gpd.read_file(results_path + file_name, layer='ElectricityProductionPlant', engine='pyogrio')
    gdf_PV = gdf_PV.to_crs(epsg=4326)
    gdf_PV = gdf_PV.loc[gdf_PV['Canton'] == 'TI']
    gdf_PV = gdf_PV.loc[gdf_PV['MainCategory'] == 'maincat_2']
    gdf_PV["year"] = np.where(gdf_PV["BeginningOfOperation"] != 0,
                              pd.to_datetime(gdf_PV["BeginningOfOperation"], errors='coerce').dt.year,
                              gdf_PV["BeginningOfOperation"])
    gdf_PV = gdf_PV.loc[~gdf_PV['year'].isin([2025])]
    gdf_PV = gdf_PV[['year', 'geometry', 'TotalPower']]
    gdf_PV = gdf_PV[gdf_PV.geometry.is_valid]
    gdf_PV['lon'] = gdf_PV.geometry.x
    gdf_PV['lat'] = gdf_PV.geometry.y
    gdf_PV = gdf_PV.loc[gdf_PV['lon'] > 7]
    gdf_PV_grouped = gdf_PV.groupby("year")["TotalPower"].sum().reset_index()
    gdf_PV_grouped["cumulata"] = gdf_PV_grouped["TotalPower"].cumsum()
    gdf_PV = gdf_PV[['lon', 'lat', 'TotalPower', 'year']]

    return gdf_PV, gdf_PV_grouped

[gdf_PV, gdf_PV_grouped] = upload_data_gdf('/ch.bfe.elektrizitaetsproduktionsanlagen.gpkg')


@st.cache_data
def upload_data_and_plot5(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', index_col=0, on_bad_lines='skip')

    df = df.transpose().reset_index()
    df = df.rename(columns={"index": "Year"})

    df["Year"] = df["Year"].astype(int)
    df_melt = df.melt('Year', var_name='Type', value_name='Nuove installazioni annue')

    fig = px.bar(df_melt, x="Year", y="Nuove installazioni annue", color="Type", barmode="group", text_auto=True)

    fig.update_layout(
        legend=dict(x=0, y=0.8, xanchor='left', yanchor='bottom', bgcolor='rgba(255,255,255,0.7)', title=None),
        title=dict(text='Nuove installazioni annue PV', x=0.5, xanchor="center", y=0.9),
        xaxis=dict(tickmode='array', tickvals=df['Year'].unique(), tickangle=45, showgrid=False),
        xaxis_title="Anno",
        yaxis_title="Nuove installazioni annue"
    )

    return fig

fig6 = upload_data_and_plot5('/plots_data/Calibration_PV.csv')


@st.cache_data
def upload_data_and_plot6(file_name):
    df = pd.read_csv(results_path + file_name, sep=';', index_col=0, on_bad_lines='skip')

    df = df.transpose().reset_index()
    df = df.rename(columns={"index": "Year"})

    df["Year"] = df["Year"].astype(int)
    df_melt = df.melt('Year', var_name='Type', value_name='Nuove installazioni annue')

    fig = px.bar(df_melt, x="Year", y="Nuove installazioni annue", color="Type", barmode="group", text_auto=True)

    fig.update_layout(
        legend=dict(x=0, y=0.8, xanchor='left', yanchor='bottom', bgcolor='rgba(255,255,255,0.7)', title=None),
        title=dict(text='Nuove installazioni annue pompe di calore', x=0.5, xanchor="center", y=0.9),
        xaxis=dict(tickmode='array', tickvals=df['Year'].unique(), tickangle=45, showgrid=False),
        xaxis_title="Anno",
        yaxis_title="Nuove installazioni annue"
    )

    return fig

fig7 = upload_data_and_plot6('/plots_data/Calibration_HP.csv')


st.set_page_config(page_title="Approccio System Dynamics", page_icon="🔄", layout="wide")

st.title("🔄 Approccio System Dynamics")

tab1, tab2, tab3, tab4 = st.tabs(["1 - Definizione problema", "2 - Modello qualitativo", "3 - Modello quantitativo", "4 - Calibrazione"])

with tab1:

    st.markdown(
        """
        ### ❓ Definizione problema
        
        L’obiettivo finale è costruire un modello che rappresenti nel modo più accurato possibile il comportamento del 
        sistema in analisi. Poiché lo studio della transizione è un problema complesso che coinvolge un sistema 
        complesso, come quello energetico, il primo passo consiste nel definire chiaramente il sistema oggetto di 
        studio, individuandone i confini e gli elementi principali.  

        Questo è ciò che abbiamo fatto durante il primo incontro, in cui abbiamo descritto gli elementi del sistema 
        sulla base delle tre categorie definite dal **Multi-Level Perspective (MLP)**:

        - **Landscape** → rappresenta il livello macro, ovvero il contesto esterno e i fattori di lungo periodo che 
        influenzano il sistema (ad esempio, tendenze socio-economiche, politiche, culturali o ambientali).  
        - **Regimi** → costituiscono il livello intermedio e comprendono le strutture, le regole e le pratiche 
        consolidate che definiscono il funzionamento del sistema attuale.  
        - **Nicchie** → sono il livello micro, dove si sviluppano innovazioni e sperimentazioni che possono, nel tempo, 
        influenzare o trasformare i regimi esistenti.
        """
    )

    st.image(results_path + "/images/Image_1.png", caption="Risultati dell'analisi svolta durante il primo workshop. Il numero"
                                                    " all'interno dei cerchi rappresenta il numero di menzioni del "
                                                    "relativo elemento.")

with tab2:

    st.markdown(
        """
        ### 🧠 Modello qualitativo
        
        Una volta definito il sistema da analizzare, con i suoi limiti e i suoi elementi principali, il passo successivo 
        consiste nella costruzione di **mappe concettuali** che rappresentano le variabili chiave del sistema in esame.  
        Per questo scopo abbiamo utilizzato i **Causal Loop Diagram (CLD)**, un approccio tipico della **System 
        Dynamics**, che consente di visualizzare le relazioni di causa-effetto tra le variabili del sistema.  
        
        L’immagine qui sotto mostra un esempio di CLD relativo alle relazioni che influenzano l’adozione dei veicoli 
        elettrici. In questi diagrammi, le variabili principali sono collegate da frecce che indicano la direzione e 
        la natura della relazione:
        
        - **“+”** → la relazione è di **diretta proporzionalità** (un aumento della variabile A causa un aumento della 
        variabile B, e viceversa).  
        - **“–”** → la relazione è di **inversa proporzionalità** (un aumento della variabile A causa una 
        diminuzione della variabile B, e viceversa).  
        
        I CLD sono strumenti molto utili per comprendere in modo qualitativo le **dinamiche del sistema** e per 
        individuare i **feedback loop**, che possono essere di due tipi:
        
        - **Balancing Loop (B)** → tende a stabilizzare il sistema, contrastando i cambiamenti e riportandolo verso 
        l’equilibrio.  
        - **Reinforcing Loop (R)** → amplifica i cambiamenti, generando effetti di crescita o declino esponenziale 
        nel sistema.
        """
    )

    st.image(results_path + "/images/Image_2.png", caption="Esempio di CLD per la diffusione di veicoli elettrici.")

with tab3:

    st.markdown(
        """
        ### 🧩 Modello quantitativo
        
        Dopo aver costruito una versione qualitativa del sistema studiato, non resta che tradurla in un modello 
        quantitativo. Per fare ciò, è necessario raccogliere dati che descrivono lo stato attuale del sistema e la sua 
        evoluzione del tempo. 
        
        Alcuni dei dati raccolti per costruire il modello sono qui rappresentati, per dare un'idea
        delle aree su cui ci siamo concentrati. I dati sono divisi in due grandi categorie: **produzione** e 
        **consumi**.
        """
    )

    tab5, tab6 = st.tabs(["Produzione", "Consumi"])

    with tab5:

        st.subheader("Produzione storica")

        st.markdown(
            """
            Di seguito sono riportati i dati di produzione anna di energia elettrica in Ticino. Sulla destra la distinzione 
            è fatta tra **idroelettrico** e la somma di tutte le altre forme di produzione. Storicamente l'idroelettrico ha 
            rappresentato la principale fonte di approvvigionamento, ma negli ultimi anni la quota di **energia solare** è 
            aumentata molto. 
            """
        )

        row1, row2, row3 = st.columns([1, 0.1, 1])
        with row1:
            st.plotly_chart(fig4.update_layout(height=450), use_container_width=True)
        with row3:
            st.plotly_chart(fig5.update_layout(height=450), use_container_width=True)

        st.subheader("🌞 Adozione pannelli fotovoltaici")

        row1, row2, row3 = st.columns([1.5, 0.1, 1])
        with row1:
            progress_bar = st.progress(0)
            status_text = st.empty()
            chart = st.line_chart([])

            for i, row in gdf_PV_grouped.iterrows():
                new_point = pd.DataFrame({"cumulata": [row["cumulata"]]}, index=[int(row["year"])])
                chart.add_rows(new_point)
                progress_bar.progress(int((i + 1) / len(gdf_PV) * 100))
                time.sleep(0.1)

            progress_bar.empty()
            st.button("Re-run")
        with row3:
            df = gdf_PV.copy()
            st.map(df, latitude="lat", longitude="lon", height=350)

    with tab6:

        st.subheader("Consumi storici per settore")

        st.markdown(
            """
            Di seguito sono riportati i **consumi storici** nel cantone per settore finale di utilizzo. Successivamente sono 
            anche riportati i dati per il consumo di elettricità nel cantone. In entrambi i casi, è possibile selezionare
            sulla destra un anno specifico per visualizzare la ripartizione dei consumi nello specifico.
            """
        )

        row1, row2, row3 = st.columns([1.5, 0.1, 1])
        with row1:
          st.plotly_chart(fig1.update_layout(height=450), use_container_width=True)
        with row3:
          year1 = st.selectbox("# Seleziona un anno per i consumi dettagliati:", df1["year"].unique(), key="year1")
          fig_pie1 = plot_pie(df1, year1)
          st.plotly_chart(fig_pie1.update_layout(height=380), use_container_width=True)


        row1, row2, row3 = st.columns([1.5, 0.1, 1])
        with row1:
          st.plotly_chart(fig2.update_layout(height=450), use_container_width=True)
        with row3:
          year2 = st.selectbox("# Seleziona un anno per i consumi dettagliati:", df2["year"].unique(), key="year2")
          fig_pie2 = plot_pie(df2, year2)
          st.plotly_chart(fig_pie2.update_layout(height=380), use_container_width=True)

        st.subheader("🏠 Settore residenziale")

        st.markdown(
            """
            Come evidente dai grafici riportati sopra, il settore residenziale è la principale fonte di consumo energetico 
            nel cantone. Di seguito è riportata una rappresentazione della raccolta dati effettuata in questo settore. 
            L'obiettivo è quello di categorizzare gli edifici in **archetipi**, in modo da comprendere gli effetti di 
            diverse politiche energetiche e scenari su diversi gruppi sociali. 
            
            Gli edifici sono stati categorizzati in base a:
            - 🏠 *Tipo di edificio*: Casa singola (SFH), bifamiliare (DFH), plurifamiliare (MFH), non residenziale.
            - ☀️ *Presenza PV*: Con o senza un impianto fotovoltaico.
            - 🔥 *Tecnologia riscaldamento*: Gas, Olio, Pompa di calore, etc.
            - 🌍 *Efficienza energetica*: Calcolata considerando il tipo di edificio e l'epoca di costruzione.
            
            Inoltre, per ogni edificio, sono stati raccolti dati riguardanti il potenziale del tetto e l'area; questi dati 
            sono stati utilizzati per calcolare la propensione all'installazione di impianti fotovoltaici ed il consumo 
            energetico per ogni archetipo.
            
            La mappa sottostante mostra la l'esempio per il comune di Massagno.
            """
            )

        st.components.v1.html(map_html, height=600, scrolling=True)

        st.markdown(
        """
        
        ❗ Conoscere la situazione attuale del sistema energetico non basta per capirne la dinamica di evoluzione ❗
        
        La raccolta di dati storici è fondamentale per comprendere i trend e analizzare i fattori che influenzano 
        maggiormente la diffusione delle nuove tecnologie. A tal fine, sono stati raccolti dati storici sull’adozione di 
        tutte le tecnologie legate al consumo di energia. In particolare, per gli edifici residenziali e per il settore 
        dei trasporti — che rappresentano la quota principale dei consumi totali nel cantone — l’attenzione si è 
        concentrata sull’adozione delle pompe di calore e dei veicoli elettrici, oltre che delle tecnologie tradizionali. 
        
        Di seguito sono riportati gli esempi di dati raccolti per le tecnologie legate al riscaldamento nel settore 
        residenziale: 
        - Installazioni annue di tutte le tecnologie (per tutto il cantone).
        - Installazioni annue di pompe di calore (diversificata per diverse catogorie).
        
        """
        )

        row1, row2, row3 = st.columns([1, 0.1, 1])
        with row1:
            st.plotly_chart(fig3.update_layout(height=450), use_container_width=True)
        with row3:
            option = st.selectbox(
                "",
                ["Tipo di edificio", "Distretto"]
            )
            if option == "Tipo di edificio":

                columns_to_plot = ["SFH", "DFH", "MFH"]
                fig = px.line(df_HP, x="Year", y=columns_to_plot, markers=True,
                              labels={"value": "Installazioni annue", "variable": "", "Year": "Anno"})
                fig.update_layout(
                    legend=dict(x=0, y=0.9, xanchor='left', yanchor='middle', bgcolor='rgba(255,255,255,0.7)'),
                    title=dict(text='Installazioni annue pompe di calore', x=0.5, xanchor="center", y=1)
                )
            else:

                columns_to_plot = ["Bellinzona", "Blenio", "Leventina", "Locarno", "Lugano", "Mendrisio", "Riviera", "Vallemaggia"]
                fig = px.line(df_HP, x="Year", y=columns_to_plot, markers=True,
                              labels={"value": "Installazioni annue", "variable": "", "Year": "Anno"})
                fig.update_layout(
                    legend=dict(x=0, y=0.8, xanchor='left', yanchor='middle', bgcolor='rgba(255,255,255,0.7)'),
                    title=dict(text='Installazioni annue pompe di calore', x=0.5, xanchor="center", y=1)
                )
            st.plotly_chart(fig.update_layout(height=370), use_container_width=True)

with tab4:

    st.markdown(
        """
        ### ⚙️ Calibrazione del modello con dati storici

        In questa sezione viene illustrato il processo di **calibrazione del modello** attraverso il confronto tra i 
        risultati simulati e i dati storici osservati.  
        La calibrazione è una fase fondamentale per verificare la **capacità del modello di rappresentare in modo 
        realistico** il comportamento del sistema reale nel tempo.  
        L’obiettivo è ridurre al minimo le differenze tra i valori simulati e quelli storici, assicurando che il modello 
        riproduca correttamente le tendenze passate prima di essere utilizzato per scenari futuri.  
        
        A titolo di esempio, vengono mostrati i risultati della calibrazione relativi a due tecnologie chiave della 
        transizione energetica:  
        - **Adozione del fotovoltaico (PV)**  
        - **Diffusione delle pompe di calore (HP)**  
        
        Questi confronti permettono di valutare la bontà della calibrazione e di individuare eventuali margini di 
        miglioramento nella rappresentazione del comportamento del sistema.
        """
    )

    row1, row2 = st.columns([1, 1])
    with row1:
        st.plotly_chart(fig6, use_container_width=True)
    with row2:
        st.plotly_chart(fig7, use_container_width=True)