# Dualfoil GUI

Python GUI to use the Dualfoil Fortran code from John Newman.
Based on Lucas Darby Robinson, R. Edwin García (2016), "Dualfoil.py: Porous Electrochemistry for Rechargeable Batteries," https://nanohub.org/resources/dualfoil. (DOI: 10.4231/D3KP7TS5M).

To run the program, use:
 python dualfoil.py

In order to compile a standalone executable, go to the bin directory and run
pyinstaller --onefile --windowed --icon="main_icon.ico" dualfoil.py --add-data "main_icon.ico;." --add-binary "dualfoil;dualfoil"
on Windows 

pyinstaller --onefile --windowed  dualfoil.py --add-data "main_icon.ico:." --add-binary "dualfoil:dualfoil"
on Unix