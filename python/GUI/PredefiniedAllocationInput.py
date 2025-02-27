import streamlit as st
from streamlit_ace import st_ace
import json
import pandas as pd


def predefiniedAllocationInput():
    inputFriendlyOption = st.radio("¿como desea ingresar la distribución inicial?",["Json", "Tabla"], horizontal=True)
    if inputFriendlyOption == "Json":
        AllocationJsonInput()
    else:
        AllocationTableInput() 
        
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

