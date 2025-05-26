import streamlit as st

from PDFGenerator import createPdf

def resultsPage():
    st.title("Resultados de la Ejecución")
    if "finalAllocation" in st.session_state and "evaluation" in st.session_state:
        st.subheader("Final Allocation")

        detailedFinalAllocation = {str(key): str(value) for key, value in st.session_state.finalAllocation.items()}
        finalAllocation = {key.id: value for key, value in st.session_state.finalAllocation.items() if value != -1}
        if(st.radio("Mostrar asignación detallada", ("Sí", "No")) == "Sí"):
            st.json(detailedFinalAllocation)
        else:
            st.json(finalAllocation)
        
        st.subheader("Evaluation")
        st.json(st.session_state.evaluation)

        if st.button("Generar PDF"):
            createPdf(st.session_state.finalAllocation)
            st.success("PDF generado con éxito.")
                    
    else:
        st.write("No hay resultados disponibles. Por favor, ejecute el algoritmo primero.")