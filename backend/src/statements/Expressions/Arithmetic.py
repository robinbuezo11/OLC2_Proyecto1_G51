from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Objects.Table import Field
from utils.TypeExp import TypeExp
from utils.DomineOp import plus, minus, mult, div
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class Arithmetic(Expression):
    def __init__(self, line: int, column: int, exp1: Expression, sign: str, exp2: Expression):
        super().__init__(line, column, TypeExp.ARITHMETIC_OP)
        self.exp1 = exp1
        self.sign = sign
        self.exp2 = exp2
        self.type: Type = Type.NULL

    def setField(self, field: dict[str, Field]) -> any:
        if self.exp1:
            self.exp1.setField(field)
        self.exp2.setField(field)

    def execute(self, env: Env) -> ReturnType:
        match self.sign:
            case '+':
                return self.plus(env)
            case '-':
                if self.exp1 != None:
                    return self.minus(env)
                return self.negative(env)
            case '*':
                return self.mult(env)
            case '/':
                return self.div(env)
            case _:
                return ReturnType('NULL', Type.NULL)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def plus(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = plus[value1.type.value][value2.type.value]
        if self.type != Type.NULL:
            if self.type == Type.BIT:
                return ReturnType(1 if int(value1.value) == 1 or int(value2.value) == 1 else 0, self.type)
            elif self.type == Type.INT:
                return ReturnType(int(int(value1.value) + int(value2.value)), self.type)
            elif self.type == Type.DECIMAL:
                return ReturnType(float(value1.value) + float(value2.value), self.type)
            elif self.type == Type.NVARCHAR or self.type == Type.NCHAR:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def minus(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = minus[value1.type.value][value2.type.value]
        if self.type != Type.NULL:
            if self.type == Type.INT:
                return ReturnType(int(value1.value) - int(value2.value), self.type)
            elif self.type == Type.DECIMAL:
                return ReturnType(float(value1.value) - float(value2.value), self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def negative(self, env: Env) -> ReturnType:
        value: ReturnType = self.exp2.execute(env)
        self.type = value.type
        if self.type == Type.INT or self.type == Type.DECIMAL:
            return ReturnType(-value.value, self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', Type.NULL)

    def mult(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = mult[value1.type.value][value2.type.value]
        if self.type == Type.BIT:
                return ReturnType(1 if int(value1.value) == 1 and int(value2.value) == 1 else 0, self.type)
        elif self.type == Type.INT:
            return ReturnType(int(value1.value) * int(value2.value), self.type)
        elif self.type == Type.DECIMAL:
            return ReturnType(float(value1.value) * float(value2.value), self.type)
        elif self.type == Type.DATE or self.type == Type.DATETIME:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        elif self.type == Type.NVARCHAR or self.type == Type.NCHAR:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def div(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = div[value1.type.value][value2.type.value]
        if self.type == Type.INT:
            if value2.value != 0:
                return ReturnType(int(float(value1.value) / float(value2.value)), self.type)    
            env.setError('No se puede dividir entre 0', self.exp2.line, self.exp2.column)
            return
        elif self.type == Type.DECIMAL:
            if value2.value != 0:
                return ReturnType(float(value1.value) / float(value2.value), self.type)
            env.setError('No se puede dividir entre 0', self.exp2.line, self.exp2.column)
            return
        elif self.type == Type.DATE or self.type == Type.DATETIME:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        elif self.type == Type.NVARCHAR or self.type == Type.NCHAR:
                return ReturnType(f'{value1.value}{value2.value}', self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnType('NULL', self.type)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.sign}"];'
        value1: ReturnAST
        if self.exp1 != None:
            value1 = self.exp1.ast(ast)
            dot += '\n' + value1.dot
            dot += f'\nnode_{id} -> node_{value1.id};'
        value2: ReturnAST = self.exp2.ast(ast)
        dot += '\n' + value2.dot
        dot += f'\nnode_{id} -> node_{value2.id};'
        return ReturnAST(dot, id)