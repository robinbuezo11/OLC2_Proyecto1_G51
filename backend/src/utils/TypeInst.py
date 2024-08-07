from enum import Enum

class TypeInst(Enum):
    PRINT          = "PRINT"
    SELECT         = "SELECT"
    INIT_ID        = "INIT_ID"
    ASIGN_ID       = "ASIGN_ID"
    BLOCK_INST     = "BLOCK_INST"
    INIT_FUNCTION  = "INIT_FUNCTION"
    IF             = "IF"
    BREAK          = "BREAK"
    CONTINUE       = "CONTINUE"
    LOOP_WHILE     = "LOOP_WHILE"
    LOOP_FOR       = "LOOP_FOR"
    CASE           = "CASE"
    WHEN           = "WHEN"
    CREATE_TABLE   = "CREATE_TABLE"
    TRUNCATE_TABLE = "TRUNCATE_TABLE"
    INSERT_TABLE   = "INSERT_TABLE"
    ALTER_TABLE    = "ALTER_TABLE"
    DELETE_TABLE   = "DELETE_TABLE"
    UPDATE_TABLE   = "UPDATE_TABLE"
    NATIVE_FUNC    = 'NATIVE_FUNC'