#setup.py
from cx_Freeze import setup, Executable

import sys 
import matplotlib
import numpy
import os
import ctypes
import timeit
import tkinter

python_install_location = 'c:\\Users\weeber\\.conda\\envs\\knowledgerules2\\'

sys.path.append(python_install_location + 'Lib\\site-packages\\mpl_toolkits\\mplot3d')
sys.path.append(python_install_location + 'Lib\\site-packages\\mpl_toolkits\\')
sys.path.append("../../scripting_library/")

base = None
#if sys.platform == "win32":
#    base = "Win32GUI"
    
executables = [Executable(r'view_edit_tool.py',base=base)]
os.environ['TCL_LIBRARY'] = python_install_location + 'Library\\lib\\tcl8.6'
os.environ['TK_LIBRARY'] = python_install_location + 'Library\\lib\\tk8.6'

setup(
    name = "view_edit_tool",
    version = "1.1.1",
    options = {"build_exe": {'packages': ["tkinter",\
        "ctypes","timeit","os","sys","copy","lxml","pandas","numpy",\
        "asteval","collections","matplotlib","blockdiag", "pkg_resources",\
        "unittest","random","copy","re", "autecology_xml","pyqt5_visualization"],
        'includes' : ["numpy","PyQt5"],
        'include_files': [r'..\..\scripting_library\AutecologyXMLtest.xml',
                          ('image','image'),
                          #you will need to manually change this if these dll's are required
                           (python_install_location +'Lib\\site-packages\\mpl_toolkits','mpl_toolkits'),
                           (python_install_location + 'Library\\bin\\mkl_intel_thread.2.dll','mkl_intel_thread.dll'),
                           (python_install_location + 'Library\\bin\\mkl_core.2.dll','mkl_core.dll'),
                           (python_install_location + 'Library\\bin\\mkl_avx.2.dll','mkl_avx.dll'),
                           (python_install_location + 'Library\\bin\\mkl_avx2.2.dll','mkl_avx2.dll'),
                           (python_install_location + 'Library\\bin\\mkl_def.2.dll','mkl_def.dll'),
                           (python_install_location + 'Library\\bin\\mkl_def.2.dll','mkl_def.dll')],
        'include_msvcr': True
    }},
    author='Marc Weeber',
    description='View edit tool for knowledgerules https://github.com/Deltares/KnowledgeRules',
    executables = executables
    )
    
 #Still need to manually add PyQt5
 #See post: https://stackoverflow.com/questions/55120281/cx-freeze-importerror-no-module-named-pyqt5-qt
 #Copy PyQt5 from site packages and add to \build\exe.win'SPECIFIC'\lib'
 #
 #Manually need to copy before running setup.py build:
 #..\Library\bin\tk86t.dll -> ..\DLLs\tk86t.dll
 #..\Library\bin\tcl86t.dll -> ..\DLLs\tcl86t.dll
 #
 #Before making the bdist_msi, you might need to remove the exe build to not get an error.
