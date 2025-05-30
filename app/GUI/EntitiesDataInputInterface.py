import streamlit as st
from streamlit_ace import st_ace
import json
from ConfigurationVars  import INPUT_DATA_FILE_PATH 

def entitiesDataInput():
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
    with open(INPUT_DATA_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
