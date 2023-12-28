from statements.Objects.Table import Field
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type
from utils.TypeExp import TypeExp
from statements.Env.AST import AST, ReturnAST
from statements.Abstracts.Expression import Expression
from statements.Env.Env import Env

class Relational(Expression):
    def __init__(self, line: int, column: int, exp1: Expression, sign: str, exp2: Expression):
        super().__init__(line, column, TypeExp.RELATIONAL_OP)
        self.exp1 = exp1
        self.sign = sign
        self.exp2 = exp2

    def setField(self, field: dict[str, Field]) -> any:
        self.exp1.setField(field)
        self.exp2.setField(field)

    def execute(self, env: Env) -> ReturnType:
        match self.sign:
            case '==':
                return self.equal(env)
            case '=':
                return self.equal(env)
            case '!=':
                return self.notEqual(env)
            case '>=':
                return self.greatEqual(env)
            case '<=':
                return self.lessEqual(env)
            case '>':
                return self.great(env)
            case '<':
                return self.less(env)
            case _:
                return ReturnType('NULL', Type.NULL)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def equal (self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return ReturnType(value1.value == value2.value, Type.BOOLEAN)
            env.setError("Los tipos no son válidos para operaciones relacionales (==)", self.exp2.line, self.exp2.column)
            return ReturnType('NULL', Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return ReturnType(value1.value == value2.value, Type.BOOLEAN)
        env.setError("Los tipos no son válidos para operaciones relacionales (==)", self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def notEqual(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        if value1.type == Type.INT or value1.type == Type.DECIMAL:
            if value2.type == Type.INT or value2.type == Type.DECIMAL:
                return ReturnType(value1.value != value2.value, Type.BOOLEAN)
            env.setError("Los tipos no son válidos para operaciones relacionales (!=)", self.exp2.line, self.exp2.column)
            return ReturnType('NULL', Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return ReturnType(value1.value != value2.value, Type.BOOLEAN)
        env.setError("Los tipos no son válidos para operaciones relacionales (!=)", self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def greatEqual(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return ReturnType(value1.value >= value2.value, Type.BOOLEAN)
            env.setError("Los tipos no son válidos para operaciones relacionales (>=)", self.exp2.line, self.exp2.column)
            return ReturnType('NULL', Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return ReturnType(value1.value >= value2.value, Type.BOOLEAN)
        env.setError("Los tipos no son válidos para operaciones relacionales (>=)", self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def lessEqual(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return ReturnType(value1.value <= value2.value, Type.BOOLEAN)
            env.setError("Los tipos no son válidos para operaciones relacionales (<=)", self.exp2.line, self.exp2.column)
            return ReturnType('NULL', Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return ReturnType(value1.value <= value2.value, Type.BOOLEAN)
        env.setError("Los tipos no son válidos para operaciones relacionales (<=)", self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def great(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return ReturnType(value1.value > value2.value, Type.BOOLEAN)
            env.setError("Los tipos no son válidos para operaciones relacionales (>)", self.exp2.line, self.exp2.column)
            return ReturnType('NULL', Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return ReturnType(value1.value > value2.value, Type.BOOLEAN)
        env.setError("Los tipos no son válidos para operaciones relacionales (>)", self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def less(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return ReturnType(value1.value < value2.value, Type.BOOLEAN)
            env.setError("Los tipos no son válidos para operaciones relacionales (<)", self.exp2.line, self.exp2.column)
            return ReturnType('NULL', Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return ReturnType(value1.value < value2.value, Type.BOOLEAN)
        env.setError("Los tipos no son válidos para operaciones relacionales (<)", self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.sign}"];'
        value1: ReturnAST = self.exp1.ast(ast)
        dot += '\n' + value1.dot
        dot += f'\nnode_{id} -> node_{value1.id};'
        value2: ReturnAST = self.exp2.ast(ast)
        dot += '\n' + value2.dot
        dot += f'\nnode_{id} -> node_{value2.id};'
        return ReturnAST(dot, id)