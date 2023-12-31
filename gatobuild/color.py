from enum import Enum


# Colors
class Color(Enum):
    RESET   = '\u001b[0m'

    BLACK   = '\u001b[30m'
    RED     = '\u001b[31m'
    GREEN   = '\u001b[32m'
    YELLOW  = '\u001b[33m'
    BLUE    = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN    = '\u001b[36m'
    WHITE   = '\u001b[37m'

def printColored(text, color: Color):
    print(f'{color.value}{text}{Color.RESET.value}', end='')
