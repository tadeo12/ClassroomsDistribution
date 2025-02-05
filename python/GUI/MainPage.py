import os
from streamlit_ace import st_ace
import streamlit as st
import json
from ConfigurationVars  import *

import pandas as pd

from Logic.EjecutionHandler import ejecutionButtonHandler
from Logic.EntititiesManager import createEntitiesFromJson


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
    st.subheader("Edición de data.json")

    json_text = st_ace(st.session_state.entitiesJsonText, language='json', height=500)

    if st.button("Guardar"):
        saveInputEntitiesButtonHandler(json_text)

def saveInputEntitiesButtonHandler(entitiesJsonText):
    try:
        saveEntitiesJson(json.loads(entitiesJsonText))
        st.session_state.entitiesJsonText = entitiesJsonText
        #TODO validacion
        st.success("Archivo guardado correctamente")
    except json.JSONDecodeError:
        st.error("JSON inválido")

def saveEntitiesJson(data):
    with open(INPUT_DATA_FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


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

def predefiniedAllocationInput():
    inputFriendlyOption = st.radio("¿como desea ingresar la distribución inicial?",["Json", "Tabla"], horizontal=True)
    if inputFriendlyOption == "Json":
        AllocationJsonInput()
    else:
        AllocationTableInput() 

def AllocationTableInput():
    resources = st.session_state.entities["resources"]
    commissions = st.session_state.entities["commissions"]

    resource_dict = {r.id: r for r in resources}

    df = pd.DataFrame({
            "Resource ID": [r.id for r in resources],
            "Resource": [str(r) for r in resources],
            "Commission": [None] * len(resources)  # Inicialmente vacío
        })
    
    st.title("Asignar Comisiones a Recursos")

    st.write("Edita la columna 'Commission' para asignar una comisión a cada recurso.")

    df_editable = st.data_editor(
            df,
            column_config={
                "Commission": st.column_config.SelectboxColumn(
                    "Commission",
                    options=[repr(c) for c in commissions],  # Opciones en el selectbox
                    required=True,
                )
            },
            hide_index=True
        )

    if st.button("Guardar Asignación"):
        result = {
                resource_dict[row["Resource ID"]]: next(c for c in commissions if repr(c) == row["Commission"])
                for _, row in df_editable.iterrows()
            }
        st.success("Asignación completada:")
        st.json({repr(k): repr(v) for k, v in result.items()})

def AllocationJsonInput():
    st.subheader("Ingrese JSON para la distribución predefinida")
    predef_json = st_ace("{}", language='json', height=300)
    if st.button("Guardar distribución"):
        try:
            json.loads(predef_json)
                #TODO validacion del json
            st.success("Distribución guardada")
        except json.JSONDecodeError:
            st.error("JSON inválido") 
