import streamlit as st

# Page config (optional but nice)
st.set_page_config(page_title="Caso studio Canton Ticino", page_icon="🏞️", layout="wide")

st.title("🏞️ Caso studio Canton Ticino")

st.markdown(
    """
    Questa pagina introduce il **modello cantonale** sviluppato nell’ambito del progetto **Sustainable and Resilient 
    Energy for Switzerland (SURE)**. L’obiettivo del modello è fornire uno **strumento di supporto alle decisioni** 
    per aiutare i decisori a livello cantonale a **valutare le conseguenze di diverse azioni e politiche energetiche** 
    sul sistema energetico ticinese.  
    
    Il contenuto della pagina è suddiviso in due sezioni principali:
    
    - **🔁 Approccio System Dynamics**  
      In questa sezione viene presentato in modo sintetico l’approccio modellistico adottato per la costruzione del 
      modello cantonale, basato sulla **System Dynamics**, che permette di analizzare le interazioni e le dinamiche tra 
      i diversi elementi del sistema energetico nel tempo.
    
    - **📊 Esempio di simulazioni e risultati**  
      In questa sezione sono mostrati alcuni esempi di **simulazioni e risultati** relativi a sottosettori specifici. 
      Questi esempi servono per fornire un’idea del tipo di analisi e delle potenzialità del modello sviluppato.
    
    ---

    💡 L’obiettivo complessivo è offrire una **visione integrata e dinamica del sistema energetico cantonale**, utile 
    per pianificare strategie di transizione verso un futuro più sostenibile e resiliente.
    """
)