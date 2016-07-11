# Installer for pyAPS Library
# Note - You must have Python oreviously installed on your system

import sys, os
from shutil import copyfile

python_exe = sys.executable
python_dir = sys.exec_prefix

python_lib_dir = python_dir + os.sep + 'Lib'
python_lib_installed = python_lib_dir + os.sep + 'pyAPS.py'

source_dir = os.path.dirname(os.path.realpath(__file__))
source_code = source_dir + os.sep + 'pyAPS.py'

# Check whether install directory is correct
install_here = raw_input("Install here? " + python_lib_dir + " (y/n): ")

if install_here.lower() == 'y':
    
    # Continue with install
    #copyfile(source_code, python_lib_dir)
    print source_code
    print python_lib_installed

    print "pyAPS successfully installed."
    
