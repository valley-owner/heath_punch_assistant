import colorama
from colorama import Fore, Back, Style # 命令行颜色字体库
colorama.init(autoreset=True) # 使旧版cmd中命令行颜色字体生效, 并在print换行处自动还原默认颜色


def red(some_str):
    return Fore.LIGHTRED_EX + some_str + Fore.RESET


def yellow(some_str):
    return Fore.YELLOW + some_str + Fore.RESET


def blue(some_str):
    return Fore.LIGHTBLUE_EX + some_str + Fore.RESET


def green(some_str):
    return Fore.GREEN + some_str + Fore.RESET


def magenta(some_str):
    return Fore.MAGENTA + some_str + Fore.RESET


def cyan(some_str):
    return Fore.CYAN + some_str + Fore.RESET


def white(some_str):
    return Fore.WHITE + some_str + Fore.RESET


def reset(some_str):
    return Fore.RESET + some_str + Fore.RESET


if __name__ == '__main__':
    print(red('红色'))
    print(yellow('黄色'))
    print(blue('蓝色'))
    print(green('绿色'))
    print(magenta('粉色'))
    print(cyan('青色'))
    print(white('灰色'))
    print(reset('白色'))

