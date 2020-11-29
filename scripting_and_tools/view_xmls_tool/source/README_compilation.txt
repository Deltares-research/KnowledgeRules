#Compilation advice
https://fernandofreitasalves.com/how-to-create-python-exe-with-msi-installer-and-cx_freeze/
https://stackoverflow.com/questions/49024118/how-to-make-exe-with-cx-freeze-including-pyqt5-and-opencv-on-windows-10
https://stackoverflow.com/questions/55120281/cx-freeze-importerror-no-module-named-pyqt5-qt

#current method - build in source folder and copy over to compiled folder
python setup.py build
python setup.py bdist_msi
