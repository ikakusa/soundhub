import colorama
from colorama import Fore, Back, Style

class Logger():
    @staticmethod
    def warn(text: str):
        print(f"[{Fore.YELLOW}Warning{Fore.RESET}] {text}")
    @staticmethod
    def error(text: str):
        print(f"[{Fore.RED}Error{Fore.RESET}] {text}")
    @staticmethod
    def log(text: str):
        print(f"[Log] {text}")