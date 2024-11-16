import os
import sys
import argparse
import platform
import subprocess
import ImageTooker as ima

from check import installs
from colorama import Fore, just_fix_windows_console

INFO = 1
WARN = 2
ERROR = 3

def log(message="", type: int = INFO):
    type_text = ""
    if message:
        if type == INFO:
            type_text = f"{Fore.CYAN}[INFO] {message}"
        elif type == WARN:
            type_text = f"{Fore.YELLOW}[WARN] {message}"
        elif type == ERROR:
            type_text = f"{Fore.RED}[ERROR] {message}"
        print(type_text)

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
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))

    if platform.system() == "Windows":
        current_path = os.environ.get('PATH', '')
        if script_directory not in current_path:
            try:
                subprocess.run(f'setx PATH "{current_path};{script_directory}"', shell=True)
                print(f"Added {script_directory} to PATH")
            except Exception as e:
                print(f"Failed to add to PATH: {e}")
        else:
            print(f"{script_directory} is already in PATH.")
    
    elif platform.system() in ["Linux", "Darwin"]:
        shell_config_files = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")]
        
        for config_file in shell_config_files:
            if os.path.exists(config_file):
                with open(config_file, "a") as file:
                    file.write(f'\n# Added by ScrapyPix\nexport PATH="$PATH:{script_directory}"\n')
                print(f"Added {script_directory} to PATH in {config_file}")
                break
        else:
            print("Neither .bashrc nor .zshrc found. Please manually add the script's directory to PATH.")
    else:
        print("This script only adds to PATH on Windows or Unix-based systems.")

def main():
    add_to_path()

    args = parse_args()
    inscode = installs()
    system = platform.system()

    if not __name__.__eq__("__main__") or inscode == 0:
        exit(0)
    else:
        inscode = None
        del inscode
        del args
        del system

    if system == "Windows":
        just_fix_windows_console()

    URL = args.url
    DOWNLOAD_PATH = args.path
    DELAY = args.delay
    MAX_IMAGES = args.max

    log("Starting scraping", INFO)

    try:
        data = ima.scrape_images(URL, DOWNLOAD_PATH, DELAY, MAX_IMAGES)
        log(f"Program ended ({data})")
    except KeyboardInterrupt:
        pass
    except Exception as exception:
        log(f"Exception: {exception}", ERROR)

    URL = None
    DOWNLOAD_PATH = None
    DELAY = None
    MAX_IMAGES = None

    del args
    del system

if __name__ == "__main__":
    main()
