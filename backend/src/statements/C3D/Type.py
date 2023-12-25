from enum import Enum, auto

class Type(Enum):
    ASIGN        = 'Asign'
    CALLFUNCTION = 'CallFunction'
    END          = 'End'
    EXPRESSION   = 'Expression'
    FUNCTION     = 'Function'
    GENERIC      = 'Generic'
    GETHEAP      = 'Getheap'
    GETSTACK     = 'GETSTACK'
    GOTO         = 'Goto'
    IF           = 'If'
    LABEL        = 'Label'
    PRINTF       = 'Printf'
    RETURN       = 'Return'
    SETHEAP      = 'SetHeap'
    SETSTACK     = 'SetStack'

    def __init__(self, value):
        self.value = value

    def getValue(self):
        return self.value