import os
import re
import streamlit as st
import shutil

CONFIG_FILE = "ConfigurationVars.py"
CONSTRAINTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Constraints"))
ACTIVATED_FOLDER = os.path.join(CONSTRAINTS_FOLDER, "Enabled")
DISABLED_FOLDER = os.path.join(CONSTRAINTS_FOLDER, "Disabled")


# Función para cargar variables del archivo de configuración
def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*)$", line.strip())
                if match:
                    var_name, var_value = match.groups()
                    # Intentamos evaluar el valor de manera segura
                    try:
                        parsed_value = eval(var_value, {"__builtins__": {}})
                    except Exception:
                        parsed_value = var_value.strip('"').strip("'")  # Dejar como string si hay error
                    config[var_name] = parsed_value
    return config

# Función para guardar variables en el archivo de configuración
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        for key, value in config.items():
            if isinstance(value, str):
                f.write(f'{key} = "{value}"\n')
            else:
                f.write(f"{key} = {value}\n")

# Función para obtener restricciones activadas y desactivadas
def get_constraints():
    activated = [f for f in os.listdir(ACTIVATED_FOLDER) if f.endswith("Evaluator.py")]
    disabled = [f for f in os.listdir(DISABLED_FOLDER) if f.endswith("Evaluator.py")]
    return activated, disabled

# Función para mover restricciones entre activadas y desactivadas
def move_constraint(file, source_folder, target_folder):
    src_path = os.path.join(source_folder, file)
    dest_path = os.path.join(target_folder, file)
    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)

# Página de configuración avanzada
def advancedConfigurationPage():
    st.subheader("Configuración del algoritmo")
    st.write("Modificar solo si sabes lo que estás haciendo.")

    # Cargar configuración actual
    config = load_config()
    new_config = {}

    # Mostrar cada variable con un campo de entrada adecuado
    for key, value in config.items():
        if isinstance(value, int):
            new_config[key] = st.number_input(f"{key}", value=value, step=1)
        elif isinstance(value, float):
            new_config[key] = st.number_input(f"{key}", value=value, step=0.01)
        elif isinstance(value, bool):
            new_config[key] = st.checkbox(f"{key}", value=value)
        else:
            new_config[key] = st.text_input(f"{key}", value=str(value))

    # Guardar cambios
    if st.button("Guardar configuración"):
        save_config(new_config)
        st.success("Archivo de configuración guardado")

    # Sección de gestión de restricciones
    st.subheader("Gestión de Restricciones")
    activated, disabled = get_constraints()

    st.write("Selecciona qué restricciones quieres activar o desactivar.")
    
    # Checkbox para restricciones activadas
    selected_activated = st.multiselect("Restricciones activadas", activated + disabled, activated)
    
    # Botón para aplicar cambios en restricciones
    if st.button("Actualizar restricciones"):
        for file in activated:
            if file not in selected_activated:
                move_constraint(file, ACTIVATED_FOLDER, DISABLED_FOLDER)

        for file in disabled:
            if file in selected_activated:
                move_constraint(file, DISABLED_FOLDER, ACTIVATED_FOLDER)

        st.success("Restricciones actualizadas. Reinicia la aplicación para aplicar cambios.")