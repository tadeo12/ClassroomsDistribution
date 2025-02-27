import streamlit as st

def resultsPage():
    st.title("Resultados de la Ejecución")
    if "finalAllocation" in st.session_state and "evaluation" in st.session_state:
        st.subheader("Final Allocation")

        final_allocation_serializable = {str(key): str(value) for key, value in st.session_state.finalAllocation.items()}
        st.json(final_allocation_serializable)
        
        st.subheader("Evaluation")
        st.json(st.session_state.evaluation)
    else:
        st.write("No hay resultados disponibles. Por favor, ejecute el algoritmo primero.")