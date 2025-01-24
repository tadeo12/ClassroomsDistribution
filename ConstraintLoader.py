import os
import importlib.util
import logging


def import_file(folder, file):
    """Importa dinámicamente un archivo como módulo."""
    try:
        file_path = os.path.join(folder, file)
        module_name = file[:-3] 
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, module_name
    except Exception as e:
        logging.error(f"Error al importar el archivo {file} desde '{folder}': {e}")
        return None, None

def load_evaluation_functions():
    """Carga funciones 'evaluate' de módulos en la carpeta 'Constraints'."""
    folder = "Constraints"
    functions = {}

    if not os.path.exists(folder):
        logging.error(f"La carpeta '{folder}' no existe.")
        return {}

    for file in os.listdir(folder):
        if file.endswith("Evaluator.py") and file != "BaseEvaluator.py":
            module, module_name = import_file(folder, file)
            if module and hasattr(module, "evaluate") and callable(getattr(module, "evaluate")):
                functions[module_name] = getattr(module, "evaluate")
                logging.info(f"Se cargó correctamente la función 'evaluate' del archivo '{file}'.")
            else:
                logging.warning(f"El archivo '{file}' no tiene una función 'evaluate' callable.")

    return functions

