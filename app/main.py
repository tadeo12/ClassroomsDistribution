#from Models import *
#from RecocidoSimulado import *
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from app.GUI.Gui import main

if __name__ == "__main__":
    main()