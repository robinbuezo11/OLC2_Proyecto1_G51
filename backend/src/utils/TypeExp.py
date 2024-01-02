from enum import Enum

class TypeExp(Enum):
    PRIMITIVE     = "PRIMITIVE"
    ARITHMETIC_OP = "ARITHMETIC_OP"
    LOGIC_OP      = "LOGIC_OP"
    RELATIONAL_OP = "RELATIONAL_OP"
    ACCESS_ID     = "ACCESS_ID"
    NATIVE_FUNC   = "NATIVE_FUNC"
    CAST          = "CAST"
    PARAMETER     = "PARAMETER"
    CALL_FUNC     = "CALL_FUNC"
    RETURN        = "RETURN"
    FIELD         = "FIELD"