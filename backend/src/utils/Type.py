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

    def __str__(self) -> str:
        return f'{self.type}: {self.value}'

class ReturnC3D:
    def __init__(self, isTmp: bool = None, strValue: str = None, type: Type = None, trueLbl: str = None, falseLbl: str = None, isTrue: bool = None):
        self.isTmp = isTmp
        self.strValue = strValue
        self.type = type
        self.trueLbl = trueLbl
        self.falseLbl = falseLbl
        self.isTrue = isTrue