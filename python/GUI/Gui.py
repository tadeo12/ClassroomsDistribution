import streamlit as st

from .ResultsPage import resultsPage
from .AdvancedConfigurationPage import advancedConfigurationPage
from .MainPage import mainPage

def main(): 
    st.set_page_config(page_title="Generacion de distribucion de aulas", page_icon="../Resources/icon.png",layout="wide")  # Mejor uso del espacio
    st.sidebar.image("../Resources/logo uns.png",clamp = True ,caption="logo uns")
    
    menu_options = ["Inicio", "Opciones Avanzadas"]

 # Agregar "Resultados" si los resultados están disponibles
    if "finalAllocation" in st.session_state and "evaluation" in st.session_state:
        menu_options.append("Resultados")

    menu = st.sidebar.radio("Menú", menu_options)  

    if menu == "Inicio":
        mainPage()
    elif menu == "Opciones Avanzadas":
        advancedConfigurationPage()
    elif menu == "Resultados":
        resultsPage()  # Llamar a la nueva función de resultados
