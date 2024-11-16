from colorama import Fore

INFO = 1
WARN = 2
ERROR = 3
SUCCESS = 4
DEBUG = 5

def log(message="", type: int = DEBUG):
    type_text = f"{Fore.LIGHTWHITE_EX}{message}"
    if message:
        match type:
            case 1:
                type_text = f"{Fore.CYAN}[INFO] {message}"
            case 2:
                type_text = f"{Fore.YELLOW}[WARN] {message}"
            case 3:
                type_text = f"{Fore.RED}[ERROR] {message}"
            case 4:
                type_text = f"{Fore.GREEN}[SUCCESS] {message}"
            case 5:
                type_text = f"{Fore.LIGHTWHITE_EX}{message}"

    print(type_text, Fore.RESET)
