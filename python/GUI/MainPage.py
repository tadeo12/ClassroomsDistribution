import os
from streamlit_ace import st_ace
import streamlit as st
import json
from ConfigurationVars  import *

from Logic.EjecutionHandler import ejecutionButtonHandler
from Logic.EntititiesManager import createEntitiesFromJson
from .EntitiesDataInputInterface import entitiesDataInput

from .PredefiniedAllocationInput import predefiniedAllocationInput

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
    st.session_state.setdefault("entitiesJsonText", json.dumps(loadEntitiesJson(), indent=4))


def loadEntities():
    st.session_state.entities = createEntitiesFromJson(loadEntitiesJson())

def loadEntitiesJson():
    if os.path.exists(INPUT_DATA_FILE_PATH):
        with open(INPUT_DATA_FILE_PATH, "r") as f:
            return json.load(f)
    return {}

def leftColumnContent():
    entitiesDataInput()

def rigthColumnContent():
    st.subheader("Distribución inicial")
    initialOptionSelector = st.radio("seleccion de distribución inicial", ["Predefinida", "Aleatoria"], index=1)
    st.session_state.setdefault
    newWidth = 5 if initialOptionSelector == "Predefinida" else 8
    if newWidth != st.session_state.colWidth:
        st.session_state.colWidth = newWidth
        st.rerun()  

    if initialOptionSelector == "Predefinida":
       predefiniedAllocationInput()
    
    if st.button("Ejecutar algoritmo"):
        with st.spinner("Ejecutando algoritmo..."):     
            ejecutionButtonHandler()

