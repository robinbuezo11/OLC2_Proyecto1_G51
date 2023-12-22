from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.Type import Type
from utils.TypeInst import TypeInst

class AlterTable(Instruction):
    def __init__(self, line: int, column: int, id: str, action: str, field1: str, field2: str, type: Type):
        super().__init__(line, column, TypeInst.ALTER_TABLE)
        self.id = id
        self.action = action
        self.field1 = field1
        self.field2 = field2
        self.type = type

    def execute(self, env: Env) -> any:
        if self.action.lower() == 'add':
            env.addColumn(self.id, self.field1, self.type, self.line, self.column)
            return
        if self.action.lower() == 'drop':
            env.dropColumn(self.id, self.field1, self.line, self.column)
            return
        if self.action.lower() == 'renameto':
            env.renameTo(self.id, self.field1, self.line, self.column)
        if self.action.lower() == 'renamecolumn':
            env.renameColumn(self.id, self.field1, self.field2, self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="ALTER TABLE"];'
        match self.action.lower():
            case 'add':
                dot += f'node_{id}_action[label="ADD"];'
                dot += f'\nnode_{id}_table[label="{self.id}"];'
                dot += f'\nnode_{id}_field1[label="{self.field1}"];'
                dot += f'\nnode_{id}_type[label="{self.getType(self.type)}"];'
                dot += f'\nnode_{id}_action -> node_{id}_table;'
                dot += f'\nnode_{id}_action -> node_{id}_field1;'
                dot += f'\nnode_{id}_action -> node_{id}_type;'
            case 'drop':
                dot += f'node_{id}_action[label="DROP"];'
                dot += f'\nnode_{id}_table[label="{self.id}"];'
                dot += f'\nnode_{id}_field1[label="{self.field1}"];'
                dot += f'\nnode_{id}_action -> node_{id}_table;'
                dot += f'\nnode_{id}_action -> node_{id}_field1;'
            case 'renameto':
                dot += f'node_{id}_action[label="RENAME TO"];'
                dot += f'\nnode_{id}_table[label="{self.id}"];'
                dot += f'\nnode_{id}_field1[label="{self.field1}"];'
                dot += f'\nnode_{id}_action -> node_{id}_table;'
                dot += f'\nnode_{id}_action -> node_{id}_field1;'
            case 'renamecolumn':
                dot += f'node_{id}_action[label="RENAME COLUMN"];'
                dot += f'\nnode_{id}_table[label="{self.id}"];'
                dot += f'\nnode_{id}_field1[label="{self.field1}"];'
                dot += f'\nnode_{id}_field2[label="{self.field2}"];'
                dot += f'\nnode_{id}_action -> node_{id}_table;'
                dot += f'\nnode_{id}_action -> node_{id}_field1;'
                dot += f'\nnode_{id}_action -> node_{id}_field2;'
        dot += f'\nnode_{id} -> node_{id}_action;'
        return ReturnAST(dot, id)

    def getType(type: Type) -> str:
        match type:
            case Type.INT:
                return "INT"
            case Type.DOUBLE:
                return "DOUBLE"
            case Type.VARCHAR:
                return "VARCHAR"
            case Type.BOOLEAN:
                return "BOOLEAN"
            case Type.DATE:
                return "DATE"
            case Type.TABLE:
                return "TABLE"
            case _:
                return "NULL"