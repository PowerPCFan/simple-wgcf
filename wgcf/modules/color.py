from colorama import Fore, Style, init

init(autoreset=True)


def red(text) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def green(text) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def yellow(text) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"


def blue(text) -> str:
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"


def magenta(text) -> str:
    return f"{Fore.MAGENTA}{text}{Style.RESET_ALL}"


def cyan(text) -> str:
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}"


def white(text) -> str:
    return f"{Fore.WHITE}{text}{Style.RESET_ALL}"
