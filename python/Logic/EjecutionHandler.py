import streamlit as st
from .AllocationValidation import validate
from .RandomInitialAllocationGenerator import generateRandomInitialAllocation
from .SimulatedAnnealing import simulatedAnnealing
from .Evaluator import evaluate


def ejecutionButtonHandler(initialAllocation: dict = None):
    commissions = st.session_state.entities["commissions"]
    resources = st.session_state.entities["resources"]
     
    if not initialAllocation:
        initialAllocation = generateRandomInitialAllocation(commissions, resources)
    else:
        validate(initialAllocation)

    st.session_state["finalAllocation"] = simulatedAnnealing(initialAllocation)
    st.session_state["evaluation"] = evaluate(st.session_state["finalAllocation"])

    st.rerun()




    