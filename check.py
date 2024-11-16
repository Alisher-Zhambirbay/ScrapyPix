import os
import subprocess
from datetime import datetime

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
                
            print("Requirements installed successfully and date saved.")
            
            return 1
        except Exception as exception:
            print(f"Error in installs: {exception}")
            return 0
    else:
        print(f"Cannot find the requirement file ({requirements}).")
        return 0
