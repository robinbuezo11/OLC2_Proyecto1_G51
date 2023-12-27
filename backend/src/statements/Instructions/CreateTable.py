from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Objects.Table import Table
from utils.TypeInst import TypeInst
from utils.Attribute import Attribute
from utils.ForeignKey import ForeignKey
from utils.Global import *
from utils.Type import Type

class CreateTable(Instruction):
    def __init__(self, line: int, column: int, name: str, attribs: list[Attribute | ForeignKey]):
        super().__init__(line, column, TypeInst.CREATE_TABLE)
        self.name = name
        self.attribs = attribs

    def execute(self, env: Env) -> any:
        table = Table(self.name.lower(), self.attribs)
        env.saveTable(self.name, table, self.line, self.column)
        
        #-----------------XML------------------
        xml.createTable(getUsedDatabase(), self.name.lower())
        for attrib in self.attribs:
            if type(attrib) == Attribute:
                xml.createColumn(getUsedDatabase(), self.name.lower(), attrib.id, self.getTypeOf(attrib.type).lower(), attrib.length, attrib.props['notNull'], attrib.props['primaryKey'])

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="TABLE"];'
        dot += f'\nnode_{id}_name[label="{self.name}"]'
        dot += f'\nnode_{id}_fields[label="CAMPOS"]'
        for i in range(len(self.attribs)):
            if type(self.attribs[i]) == Attribute:
                dot += f'\nnode_{id}_field_{i}[label={self.attribs[i].id}]'
                dot += f'\nnode_{id}_fields -> node_{id}_field_{i};'
            elif type(self.attribs[i]) == ForeignKey:
                pass
        dot += f'\nnode_{id} -> node_{id}_name;'
        dot += f'\nnode_{id} -> node_{id}_fields;'
        return ReturnAST(dot, id)
    
    def getTypeOf(self, type: Type) -> str:
        match type:
            case Type.INT:
                return "INT"
            case Type.DECIMAL:
                return "DECIMAL"
            case Type.NCHAR:
                return "NCHAR"
            case Type.NVARCHAR:
                return "NVARCHAR"
            case Type.BIT:
                return "BIT"
            case Type.DATE:
                return "DATE"
            case Type.TABLE:
                return "TABLE"
            case _:
                return "NULL"