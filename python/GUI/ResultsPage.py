import streamlit as st

def resultsPage():
    st.title("Resultados de la Ejecución")
    if "finalAllocation" in st.session_state and "evaluation" in st.session_state:
        st.subheader("Final Allocation")
        st.json(st.session_state.finalAllocation)
        
        st.subheader("Evaluation")
        st.json(st.session_state.evaluation)
    else:
        st.write("No hay resultados disponibles. Por favor, ejecute el algoritmo primero.")