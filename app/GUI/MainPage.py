import os
from streamlit_ace import st_ace
import streamlit as st
import json
from ConfigManager import ConfigManager
from app.Logic.EjecutionHandler import ejecutionButtonHandler
from app.Logic.EntititiesInitializer import createEntitiesFromJson
from app.GUI.EntitiesDataInputInterface import entitiesDataInput
from app.GUI.PredefiniedAllocationInput import showPredefiniedAllocationInput

def mainPage():
    loadSessionStateVariables()
    st.title("Generación de distribución de aulas")

    col1, col2 = st.columns([st.session_state.colWidth, 10 - st.session_state.colWidth])
    with col1:
        leftColumnContent()
    with col2:
        rigthColumnContent()


def loadSessionStateVariables():
    st.session_state.setdefault("colWidth", 7)
    st.session_state.setdefault("entities", loadEntities())
    st.session_state.setdefault("entitiesJsonText", json.dumps(loadEntitiesJson(), indent=4, ensure_ascii=False))


def loadEntities():
    st.session_state.entities = createEntitiesFromJson(loadEntitiesJson())

def loadEntitiesJson():
    inputDataFilePath = ConfigManager().getConfig()["INPUT_DATA_FILE_PATH"]
    if os.path.exists(inputDataFilePath):
        with open(inputDataFilePath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def leftColumnContent():
    entitiesDataInput()

def rigthColumnContent():
    st.subheader("Distribución inicial")
    initialOptionSelector = st.radio("seleccion de distribución inicial", ["Predefinida", "Aleatoria"], index=1, key="allocation_type")
    newWidth = 5 if initialOptionSelector == "Predefinida" else 8
    if newWidth != st.session_state.colWidth:
        st.session_state.colWidth = newWidth
        st.rerun()  

    if initialOptionSelector == "Predefinida":
       showPredefiniedAllocationInput()


    progressPlaceholder = st.empty()
    overlayPlaceholder = st.empty()
    if st.button("Ejecutar"):
   #     overlayPlaceholder.markdown("""
   #     <div style="
   #         position: fixed; top: 0; left: 0;
   #         width: 100%; height: 100%;
   #         background-color: rgba(0, 0, 0, 0.6);
   #         display: flex; flex-direction: column;
   #         justify-content: center; align-items: center;
   #         z-index: 9999; color: white; font-size: 24px;">
   #         <div id="loading-text">⏳ Procesando... </div>
   #     </div>
   # """, unsafe_allow_html=True)
        progressBar = progressPlaceholder.progress(0, text="Iniciando...")
        def updateProgress(p, cost):
            progressBar.progress(p, text=f"Progreso: {p}%  Mejor penalizacion: {cost}")
        ejecutionButtonHandler(updateProgress)
        progressPlaceholder.empty()
#    overlayPlaceholder.empty()
        st.success("El algoritmo finalizó")


