# Dualfoil GUI

Python GUI to use the Dualfoil Fortran code from John Newman.
This is an adaption of the code by Lucas Darby Robinson, R. Edwin García (2016), "Dualfoil.py: Porous Electrochemistry for Rechargeable Batteries," https://nanohub.org/resources/dualfoil. (DOI: 10.4231/D3KP7TS5M).

## Run the program
In the bin directory, run

`python dualfoil.py`

## Compile a standalone
on Windows

`pyinstaller --onefile --windowed --icon="main_icon.ico" dualfoil.py --add-data "main_icon.ico;." --add-binary "dualfoil;dualfoil"`
 
on Unix

`pyinstaller --onefile --windowed  dualfoil.py --add-data "main_icon.ico:." --add-binary "dualfoil:dualfoil"`
