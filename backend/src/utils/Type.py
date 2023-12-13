from enum import Enum, auto

class Type(Enum):
    INT      = 0
    BIT      = 1
    DECIMAL  = 2
    DATE     = 3
    DATETIME = 4
    NCHAR    = 5
    NVARCHAR = 6
    NULL     = 7
    TABLE    = 8

class ReturnType:
    def __init__(self, value: any, type: Type):
        self.value = value
        self.type = type