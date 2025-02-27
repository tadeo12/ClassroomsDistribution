import os
import re
import streamlit as st

CONFIG_FILE = "ConfigurationVars.py"

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

# Página de configuración avanzada
def advancedConfigurationPage():
    st.subheader("Configuración del algoritmo")
    st.write("modificar solo si sabes lo que estas haciendo")
    # Cargar configuración actual
    config = load_config()
    
    # Diccionario para los nuevos valores
    new_config = {}

    # Mostrar cada variable con un campo de entrada adecuado
    for key, value in config.items():
        if isinstance(value, int):
            new_config[key] = st.number_input(f"{key}", value=value, step=1)
        elif isinstance(value, float):
            new_config[key] = st.number_input(f"{key}", value=value, step=0.01)
        elif isinstance(value, bool):
            new_config[key] = st.checkbox(f"{key}", value=value)
        else:  # Se asume string por defecto
            new_config[key] = st.text_input(f"{key}", value=str(value))

    # Guardar cambios
    if st.button("Guardar configuración"):
        save_config(new_config)
        st.success("Archivo de configuración guardado")


