import os
import streamlit as st
import shutil


from ConfigManager import ConfigManager

configManager = ConfigManager()

CONSTRAINTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Constraints"))
ACTIVATED_FOLDER = os.path.join(CONSTRAINTS_FOLDER, "Enabled")
DISABLED_FOLDER = os.path.join(CONSTRAINTS_FOLDER, "Disabled")


def get_constraints():
    activated = [f for f in os.listdir(ACTIVATED_FOLDER) if f.endswith("Evaluator.py")]
    disabled = [f for f in os.listdir(DISABLED_FOLDER) if f.endswith("Evaluator.py")]
    return activated, disabled

def move_constraint(file, source_folder, target_folder):
    src_path = os.path.join(source_folder, file)
    dest_path = os.path.join(target_folder, file)
    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)

def ConfigurationPage():
    st.subheader("Configuración del algoritmo")
    st.write("Modificar solo si sabes lo que estás haciendo.")

    config = configManager.getConfig()
    newConfig = {}

    for key, value in config.items():
        if isinstance(value, int):
            newConfig[key] = st.number_input(f"{key}", value=value, step=1)
        elif isinstance(value, float):
            if key == "temperature_reduction_coefficient":
                newConfig[key] = st.number_input(
                    f"{key}", value=value, step=0.00000000000001, format="%.16f"
                )
            else:
                newConfig[key] = st.number_input(
                    f"{key}", value=value, step=0.01
                )
        elif isinstance(value, bool):
            newConfig[key] = st.checkbox(f"{key}", value=value)
        else:
            newConfig[key] = st.text_input(f"{key}", value=str(value))

    if st.button("Guardar configuración"):
        configManager.updateConfig(newConfig)
        st.success("Archivo de configuración guardado")

    st.subheader("Gestión de Restricciones")
    activated, disabled = get_constraints()

    st.write("Selecciona qué restricciones quieres activar o desactivar.")
    
    selected_activated = st.multiselect("Restricciones activadas", activated + disabled, activated)
    
    if st.button("Actualizar restricciones"):
        for file in activated:
            if file not in selected_activated:
                move_constraint(file, ACTIVATED_FOLDER, DISABLED_FOLDER)

        for file in disabled:
            if file in selected_activated:
                move_constraint(file, DISABLED_FOLDER, ACTIVATED_FOLDER)

        st.success("Restricciones actualizadas. Reinicia la aplicación para aplicar cambios.")