#setup.py
from cx_Freeze import setup, Executable

import sys 
import matplotlib
import numpy
import os
import ctypes
import timeit
import tkinter

base = None
#if sys.platform == "win32":
#    base = "Win32GUI"
    
executables = [Executable(r'view_edit_tool.py',base=base)]
os.environ['TCL_LIBRARY'] = r'C:\Users\weeber\.conda\envs\python3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\weeber\.conda\envs\python3\tcl\tk8.6'
setup(
    name = "view_edit_tool",
    version = "1.0.0",
    options = {"build_exe": {'packages': ["tkinter",\
        "ctypes","timeit","os","sys","copy","lxml","pandas","numpy",\
        "asteval","collections","matplotlib","blockdiag", "pkg_resources",\
        "unittest","random","copy","re"],
        'include_files': [r'..\source\AutecologyXMLtest.xml'],
        'include_msvcr': True
    }},
    author='Marc Weeber',
    description='View edit tool for knowledgerules https://github.com/Deltares/KnowledgeRules',
    executables = executables
    )
    
 #Still need to manually add PyQt5
 #See post: https://stackoverflow.com/questions/55120281/cx-freeze-importerror-no-module-named-pyqt5-qt
 #Copy PyQt5 from site packages and add to \build\exe.win'SPECIFIC'\lib'