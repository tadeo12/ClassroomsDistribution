import streamlit as st
from app.Logic.AllocationValidation import validate
from app.Logic.RandomInitialAllocationGenerator import generateRandomInitialAllocation
from app.Logic.SimulatedAnnealing import simulatedAnnealing
from app.Logic.Evaluator import evaluate


def ejecutionButtonHandler(progressCallback = None):
    commissions = st.session_state.entities["commissions"]
    resources = st.session_state.entities["resources"]

    if st.session_state.allocation_type == "Aleatoria":
        initialAllocation = generateRandomInitialAllocation(commissions, resources)
    else:  # "Predefinida"
        if "initialAllocation" not in st.session_state or st.session_state.initialAllocation is None:
            st.error("Debe cargar una asignación predefinida antes de ejecutar el algoritmo.")
            return
        validate(st.session_state.initialAllocation)
        initialAllocation = st.session_state.initialAllocation

    st.session_state["finalAllocation"] = simulatedAnnealing(initialAllocation, progressCallback)
    st.session_state["evaluation"] = evaluate(st.session_state["finalAllocation"])




    