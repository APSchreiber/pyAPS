# Installer for pyAPS Library
# Note - You must have Python previously installed on your system
		
import sys, os, shutil

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        shutil.copyfile(src, dest)

python_exe = sys.executable
python_dir = sys.exec_prefix

python_lib_dir = python_dir + os.sep + 'Lib'
python_lib_installed = python_lib_dir + os.sep + 'pyAPS'

source_dir = os.path.dirname(os.path.realpath(__file__))
source_code = source_dir + os.sep + 'pyAPS'

# Check whether install directory is correct
install_here = raw_input("Install here? " + python_lib_dir + " (y/n): ")

if install_here.lower() == 'y':

    # Delete old compiled file if eists
    try:
        os.remove(python_lib_dir + os.sep + 'pyAPS' + os.sep + 'aps.pyc')
    except OSError:
        pass

    # Continue with install
    recursive_overwrite(source_code, python_lib_installed)

    print "\r\n", source_code, "->", python_lib_installed

    print "\r\nModule pyAPS successfully installed."
    
