import os
import streamlit as st

from app.GUI.ResultsPage import resultsPage
from app.GUI.AdvancedConfigurationPage import advancedConfigurationPage
from app.GUI.MainPage import mainPage

def main(): 

    # Ruta base absoluta del archivo actual
    RESOURCES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Resources")
    icon_path = os.path.join(RESOURCES_PATH, "icon.png")
    logo_path = os.path.join(RESOURCES_PATH, "logo uns.png")

    st.set_page_config(page_title="Generacion de distribucion de aulas", page_icon= icon_path,layout="wide")  # Mejor uso del espacio
    st.sidebar.image(logo_path,clamp = True, width = 200)
    
    menu_options = ["Inicio", "Opciones Avanzadas"]

    if "finalAllocation" in st.session_state and "evaluation" in st.session_state:
        menu_options.append("Resultados")

    menu = st.sidebar.radio("Menú", menu_options)  

    if menu == "Inicio":
        mainPage()
    elif menu == "Opciones Avanzadas":
        advancedConfigurationPage()
    elif menu == "Resultados":
        resultsPage()  
