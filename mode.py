
from enum import Enum

class Mode(Enum):
    NORMAL = 0
    LANGUAGE = 1
    CREATE_WORD = 2

mode = Mode.NORMAL

def set_mode(value):
    global mode
    mode = value

