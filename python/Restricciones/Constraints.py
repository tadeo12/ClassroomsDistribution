
import os
import importlib
import inspect

def import_classes():
    
    classes = {}
    folder_path = "./"
    # Listar todos los archivos .py en la carpeta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py") and file_name != "__init__.py":
            # Obtener el módulo (sin la extensión .py)
            module_name = file_name[:-3]
            
            # Cargar dinámicamente el módulo
            module = importlib.import_module(f"{folder_path.replace('/', '.')}.{module_name}")
            
            # Inspeccionar el módulo y obtener las clases definidas en él
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Asegurarse de que la clase pertenece al módulo actual
                if obj.__module__ == module.__name__:
                    classes[name] = obj
    
    return classes

# Ejemplo de uso
# Suponiendo que las restricciones están en una carpeta llamada "restrictions"
if __name__ == "__main__":
    folder = "restrictions"  # Carpeta donde están las clases
    all_classes = import_classes()
    for class_name, class_obj in all_classes.items():
        print(f"Clase encontrada: {class_name} -> {class_obj}")



def getConstraints():
     