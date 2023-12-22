import re
from statements.Objects.Table import Field
from utils.Type import ReturnType, Type
from utils.TypeExp import TypeExp
from statements.Env.AST import AST, ReturnAST
from statements.Abstracts.Expression import Expression
from statements.Env.Env import Env

class Cast(Expression):
    def __init__(self, line: int, column: int, value: Expression, destinyType: Type):
        super().__init__(line, column, TypeExp.CAST)
        self.value = value
        self.destinyType = destinyType

    def setField(self, _: dict[str, Field]) -> any:
        pass

    def execute(self, env: Env) -> ReturnType:
        value: ReturnType = self.value.execute(env)
        if value.value == Type.BIT:
            if self.destinyType == Type.INT:
                return ReturnType(int(value.value), Type.INT)
            if self.destinyType == Type.NVARCHAR:
                return ReturnType(str(value.value), Type.NVARCHAR)
            if self.destinyType == Type.NCHAR:
                return ReturnType(str(value.value), Type.NCHAR)
            env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
            return ReturnType('NULL', Type.NULL)
        
        if value.type == Type.INT:
            if self.destinyType == Type.DECIMAL:
                return ReturnType(float(value.value), Type.DECIMAL)
            if self.destinyType == Type.NVARCHAR:
                return ReturnType(str(value.value), Type.NVARCHAR)
            env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
            return ReturnType('NULL', Type.NULL)

        if value.type == Type.DECIMAL:
            if self.destinyType == Type.INT:
                return ReturnType(int(value.value), Type.INT)
            if self.destinyType == Type.NVARCHAR:
                return ReturnType(str(value.value), Type.NVARCHAR)
            if self.destinyType == Type.NCHAR:
                return ReturnType(str(value.value), Type.NCHAR)
            env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
            return ReturnType('NULL', Type.NULL)

        if value.type == Type.DATE:
            if self.destinyType == Type.NVARCHAR:
                return ReturnType(str(value.value), Type.NVARCHAR)
            if self.destinyType == Type.NCHAR:
                return ReturnType(str(value.value), Type.NCHAR)
            env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
            return ReturnType('NULL', Type.NULL)

        if value.type == Type.NVARCHAR:
            if self.destinyType == Type.INT:
                asciiz = sum(ord(character) for character in value.value)
                return ReturnType(int(asciiz), Type.INT)
            if self.destinyType == Type.BOOLEAN:
                return ReturnType(value.value.toLowerCase() == 'true', Type.BOOLEAN)
            env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
            return ReturnType('NULL', Type.NULL)

        if value.type == Type.NCHAR:
            if self.destinyType == Type.INT:
                asciiz = sum(ord(character) for character in value.value)
                return ReturnType(int(asciiz), Type.INT)
            if self.destinyType == Type.BOOLEAN:
                return ReturnType(value.value.toLowerCase() == 'true', Type.BOOLEAN)
            env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
            return ReturnType('NULL', Type.NULL)
        env.setError(f'No hay casteo de "{self.getType(value.type)}" a "{self.getType(self.destinyType)}"', self.value.line, self.value.column)
        return ReturnType('NULL', Type.NULL)

    def getType(type: Type) -> str:
        match type:
            case Type.INT:
                return "INT"
            case Type.DECIMAL:
                return "DECIMAL"
            case Type.NVARCHAR:
                return "NVARCHAR"
            case Type.BOOLEAN:
                return "BOOLEAN"
            case Type.DATE:
                return "DATE"
            case Type.TABLE:
                return "TABLE"
            case _:
                return "NULL"

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="CAST"];'
        value1: ReturnAST = self.value.ast(ast)
        dot += '\n' + value1.dot
        dot += f'\nnode_{id}_type[label="{self.getType(self.destinyType)}"];'
        dot += f'\nnode_{id} -> node_{value1.id};'
        dot += f'\nnode_{id} -> node_{id}_type;'
        return {dot: dot, id: id}