from enum import Enum, auto

class Type(Enum):
    INT     = 0
    DOUBLE  = 1
    DATE    = 2
    VARCHAR = 3
    BOOLEAN = 4
    NULL    = 5
    TABLE   = 6

class ReturnType:
    def __init__(self, value: any, type: Type):
        self.value = value
        self.type = type