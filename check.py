import os
import sys
import subprocess
from datetime import datetime

def is_win_platform():
    return sys.platform in ["win32", "cygwin", "msys"]

def is_other_platform():
    return sys.platform in ["darwin", "linux", "linux2"]

def __log__(*args):
    print(*args)

def __hide_file__(file_path, logger = __log__):
    if is_win_platform():
        try:
            subprocess.run(["attrib", "+h", "+s", file_path], check=True)
            logger(f"Hidden file on Windows: {file_path}")
        except Exception as e:
            logger(f"Failed to hide file on Windows: {e}", 3)

def installs(logger = __log__):
    """
    Checks installed requirements and saves the installation date if successful.
    This function is designed to work on both Windows and Unix-based systems.
    """
    requirements = "requirements.txt"
    installed_marker = "installed.txt"

    if os.path.exists(requirements) and os.path.isfile(requirements):
        if os.path.exists(installed_marker):
            logger("Requirements already installed.", 1)

            with open(installed_marker, 'r') as file:
                install_date = file.read().strip()
                logger(f"Last installation date: {install_date}")

            return 1

        try:
            python_executable = "python3" if is_other_platform() else "py"

            subprocess.call([
                python_executable, "-m", "pip", "install", "-r", requirements
            ])
            
            with open(installed_marker, 'w') as file:
                file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            __hide_file__(installed_marker, logger = logger)

            logger("Requirements installed successfully.", 4)
            return 1

        except Exception as exception:
            logger(f"Error in installs: {exception}", 3)
            return 0

    else:
        logger(f"Cannot find the requirement file ({requirements}).", 3)
        return 0
