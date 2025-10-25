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


def load_evaluator_classes():
    """
    Carga dinámicamente las clases de evaluación desde los archivos en la carpeta 'Constraints'.
    Cada clase puede definir internamente los métodos:
        - evaluate()
        - maxValue()
        - maxHappyValue()
    """
    from app.GUI.ConfigurationPage import ACTIVATED_FOLDER
    folder = ACTIVATED_FOLDER
    evaluator_classes = {}

    if not os.path.exists(folder):
        logging.error(f"La carpeta '{folder}' no existe.")
        return {}

    for file in os.listdir(folder):
        if file.endswith("Evaluator.py") and file != "BaseEvaluator.py":
            module, module_name = import_file(folder, file)
            if module:
                class_name = module_name  # Convención: nombre de archivo == nombre de clase
                cls = getattr(module, class_name, None)

                if cls:
                    evaluator_classes[module_name] = cls
                    logging.info(f"Clase '{class_name}' cargada correctamente desde '{file}'.")
                else:
                    logging.warning(f"El archivo '{file}' no contiene una clase '{class_name}'.")
            else:
                logging.warning(f"No se pudo importar el módulo '{file}'.")

    print("Clases de evaluadores cargadas: " + str(list(evaluator_classes.keys())))
    return evaluator_classes