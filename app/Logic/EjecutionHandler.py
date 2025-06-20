import streamlit as st
from app.Logic.AllocationValidation import validate
from app.Logic.RandomInitialAllocationGenerator import generateRandomInitialAllocation
from app.Logic.SimulatedAnnealing import simulatedAnnealing
from app.Logic.Evaluator import evaluate


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




    