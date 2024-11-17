from colorama import Fore, just_fix_windows_console

just_fix_windows_console() # oh yeah

INFO = 1
WARN = 2
ERROR = 3
SUCCESS = 4
DEBUG = 5

def log(message="", type: int = DEBUG):
    """
    :param message: Message to print
    :param type: Type of message (INFO, WARN, ERROR, SUCCESS, DEBUG)
    """
    type_text = f"{Fore.LIGHTWHITE_EX}{message}"
    
    if message:
        if type == INFO:
            type_text = f"{Fore.CYAN}[INFO] {message}"
        elif type == WARN:
            type_text = f"{Fore.YELLOW}[WARN] {message}"
        elif type == ERROR:
            type_text = f"{Fore.RED}[ERROR] {message}"
        elif type == SUCCESS:
            type_text = f"{Fore.GREEN}[SUCCESS] {message}"
        elif type == DEBUG:
            type_text = f"{Fore.LIGHTWHITE_EX}{message}"

    print(type_text, Fore.RESET)
