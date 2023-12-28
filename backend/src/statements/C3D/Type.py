from enum import Enum

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