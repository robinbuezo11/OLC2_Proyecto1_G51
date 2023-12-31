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

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        match self.sign:
            case '+':
                return self.plus_c3d(env, c3dgen)
            # case '-':
            #     if self.exp1 != None:
            #         return self.minus_c3d(env)
            #     return self.negative_c3d(env)
            # case '*':
            #     return self.mult_c3d(env)
            # case '/':
            #     return self.div_c3d(env)
            case _:
                return ReturnType('NULL', Type.NULL)

    def plus_c3d(self, env: Env, c3dgen:C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        self.type = plus[value1.type.value][value2.type.value]
        if self.type != Type.NULL:
            if self.type == Type.BIT:
                tmp: str = c3dgen.newTmp()
                trueLbl: str = c3dgen.newLbl()
                falseLbl: str = c3dgen.newLbl()
                outLbl: str = c3dgen.newLbl()
                c3dgen.addIf(value1.strValue, '==', '1', trueLbl)
                c3dgen.addIf(value2.strValue, '==', '1', trueLbl)
                c3dgen.addGoto(falseLbl)
                c3dgen.addLabel(trueLbl)
                c3dgen.addAsign(tmp, '1')
                c3dgen.addGoto(outLbl)
                c3dgen.addLabel(falseLbl)
                c3dgen.addAsign(tmp, '0')
                c3dgen.addLabel(outLbl)
                return ReturnC3D(isTmp = True, strValue = tmp, type = self.type)
            elif self.type == Type.INT:
                tmp: str = c3dgen.newTmp()
                c3dgen.addExpression(tmp, value1.strValue, '+', value2.strValue)
                return ReturnC3D(isTmp = True, strValue = tmp, type = self.type)
            elif self.type == Type.DECIMAL:
                tmp: str = c3dgen.newTmp()
                c3dgen.addExpression(tmp, value1.strValue, '+', value2.strValue)
                return ReturnC3D(isTmp = True, strValue = tmp, type = self.type)
            elif self.type == Type.NVARCHAR or self.type == Type.NCHAR:
                value1Str: str = value1.strValue
                value2Str: str = value2.strValue
                if value1.type == Type.INT or value1.type == Type.DECIMAL:
                    tmp1: str = c3dgen.newTmp()
                    c3dgen.addExpression(tmp1, 'P', '+', str(env.size))
                    c3dgen.addExpression(tmp1, tmp1, '+', '1')
                    c3dgen.addSetStack(tmp1, value1Str)
                    c3dgen.newEnv(env.size)
                    c3dgen.addCallParserString(value1.type)
                    tmp2: str = c3dgen.newTmp()
                    c3dgen.addGetStack(tmp2, 'P')
                    c3dgen.prevEnv(env.size)
                    value1Str = tmp2
                if value2.type == Type.INT or value2.type == Type.DECIMAL:
                    c3dgen.generateParserString(value2.type)
                    tmp1: str = c3dgen.newTmp()
                    c3dgen.addExpression(tmp1, 'P', '+', str(env.size))
                    c3dgen.addExpression(tmp1, tmp1, '+', '1')
                    c3dgen.addSetStack(tmp1, value2Str)
                    c3dgen.newEnv(env.size)
                    c3dgen.addCallParserString(value2.type)
                    tmp2: str = c3dgen.newTmp()
                    c3dgen.addGetStack(tmp2, 'P')
                    c3dgen.prevEnv(env.size)
                    value2Str = tmp2
                c3dgen.generateConcatString()
                tmp1: str = c3dgen.newTmp()
                c3dgen.addExpression(tmp1, 'P', '+', str(env.size))
                c3dgen.addExpression(tmp1, tmp1, '+', '1')
                c3dgen.addSetStack(tmp1, value1Str)
                c3dgen.addExpression(tmp1, tmp1, '+', '1')
                c3dgen.addSetStack(tmp1, value2Str)
                c3dgen.newEnv(env.size)
                c3dgen.addCall('_concatString')
                tmp2: str = c3dgen.newTmp()
                c3dgen.addGetStack(tmp2, 'P')
                c3dgen.prevEnv(env.size)
                return ReturnC3D(isTmp = True, strValue = tmp2, type = self.type)
        env.setError('Los tipos no son válidos para operaciones aritméticas', self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = self.type)

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