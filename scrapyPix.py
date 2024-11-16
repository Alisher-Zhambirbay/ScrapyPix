import os
import sys
import ctypes
import argparse
import subprocess
import ImageTooker as ima

from check import installs
from colorama import just_fix_windows_console
from logger import *

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

def already_in_path():
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

    if is_win_platform():
        current_path = os.environ.get('PATH', '')
        return script_directory in current_path
    
    elif is_other_platform():
        shell_config_files = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")]
        for config_file in shell_config_files:
            if os.path.exists(config_file):
                with open(config_file, "r") as file:
                    if script_directory in file.read():
                        return True
        return False
    return False

def parse_args():
    parser = argparse.ArgumentParser(description="Download files using URL.")
    parser.add_argument(
        "-u", "--url", 
        required = True, 
        help = "URL of the file to download."
    )
    parser.add_argument(
        "-p", "--path", 
        default = "downloaded/", 
        help = "Path where the file will be saved. Default is 'downloaded/'."
    )
    parser.add_argument(
        "-d", "--delay",
        default = 1,
        type = int,
        help = "Delay for image_tooker"
    )
    parser.add_argument(
        "-m", "--max",
        default = -1,
        type = int,
        help="Sets maximum images to download."
    )
    return parser.parse_args()

def add_to_path():
    if already_in_path():
        log(f"Script directory is already in PATH: {os.path.dirname(os.path.abspath(sys.argv[0]))}", INFO)
        return
    
    if not is_admin():
        log("Cannot add PATH. Programm runned not in Adming prevegies", WARN)
        return

    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

    if is_win_platform():
        current_path = os.environ.get('PATH', '')
        if script_directory not in current_path:
            try:
                subprocess.run(f'setx PATH "{current_path};{script_directory}"', shell=True)
                log(f"Added {script_directory} to PATH")
            except Exception as e:
                log(f"Failed to add to PATH: {e}")
        else:
            log(f"{script_directory} is already in PATH.")
    
    elif is_other_platform():
        shell_config_files = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")]
        
        for config_file in shell_config_files:
            if os.path.exists(config_file):
                with open(config_file, "a") as file:
                    file.write(f'\n# Added by ScrapyPix\nexport PATH="$PATH:{script_directory}"\n')
                log(f"Added {script_directory} to PATH in {config_file}")
                break
        else:
            log("Neither .bashrc nor .zshrc found. Please manually add the script's directory to PATH.")
    else:
        log("This script only adds to PATH on Windows or Unix-based systems.")

def main():
    add_to_path()

    args = parse_args()
    inscode = installs()

    if not __name__.__eq__("__main__") or inscode == 0:
        exit(0)
    else:
        inscode = None
        del inscode

    if is_win_platform():
        just_fix_windows_console()

    URL = args.url
    DOWNLOAD_PATH = args.path
    DELAY = args.delay
    MAX_IMAGES = args.max

    log("Starting scraping")

    try:
        data = ima.scrape_images(URL, DOWNLOAD_PATH, DELAY, MAX_IMAGES, logger = log)
        log(f"Program ended ({data})", SUCCESS)
    except KeyboardInterrupt:
        pass
    except Exception as exception:
        log(f"Exception: {exception}", ERROR)

    URL = None
    DOWNLOAD_PATH = None
    DELAY = None
    MAX_IMAGES = None

    del args

if __name__ == "__main__":
    main()
