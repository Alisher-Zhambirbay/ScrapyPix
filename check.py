import os
import sys
import ctypes
import subprocess
from datetime import datetime

def is_win_platform():
    return sys.platform in ["win32", "cygwin", "msys"]

def is_other_platform():
    return sys.platform in ["darwin", "linux", "linux2"]

def is_admin():
    if is_win_platform():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
        
    elif is_other_platform():
        return os.geteuid() == 0

def installs():
    """
    Checks installed requirements and saves the installation date if successful.
    """
    requirements = "requirements.txt"
    installed_marker = "installed.txt"

    if os.path.exists(requirements) and os.path.isfile(requirements):
        if os.path.exists(installed_marker):
            print("Requirements already installed.")

            with open(installed_marker, 'r') as file:
                install_date = file.read().strip()
                print(f"Last installation date: {install_date}")
            return 1
        
        try:
            subprocess.call([
                "py", "-m", "pip", "install", "-r", "requirements.txt"
            ])
            
            with open(installed_marker, 'w') as file:
                file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            return 1
        except Exception as exception:
            print(f"Error in installs: {exception}")
            return 0
    else:
        print(f"Cannot find the requirement file ({requirements}).")
        return 0
