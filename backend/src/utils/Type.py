from enum import Enum, auto

class Type(Enum):
    BIT      = 0
    INT      = 1
    DECIMAL  = 2
    DATE     = 3
    DATETIME = 4
    NCHAR    = 5
    NVARCHAR = 6
    BOOLEAN  = 7
    NULL     = 8
    TABLE    = 9

class ReturnType:
    def __init__(self, value: any, type: Type):
        self.value = value
        self.type = type