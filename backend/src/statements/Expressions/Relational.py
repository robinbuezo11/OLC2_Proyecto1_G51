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

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        match self.sign:
            case '==':
                return self.equal_c3d(env, c3dgen)
            case '=':
                return self.equal_c3d(env, c3dgen)
            case '!=':
                return self.notEqual_c3d(env, c3dgen)
            case '>=':
                return self.greatEqual_c3d(env, c3dgen)
            case '<=':
                return self.lessEqual_c3d(env, c3dgen)
            case '>':
                return self.great_c3d(env, c3dgen)
            case '<':
                return self.less_c3d(env, c3dgen)
            case _:
                return ReturnC3D(isTmp = False, type = Type.NULL)

    def equal_c3d (self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return self.compare(value1.strValue, '==', value2.strValue, c3dgen)
            env.setError("Los tipos no son válidos para operaciones relacionales (==)", self.exp2.line, self.exp2.column)
            return ReturnC3D(isTmp = False, type = Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return self.compareStr(value1.strValue, '==', value2.strValue, c3dgen)
        env.setError("Los tipos no son válidos para operaciones relacionales (==)", self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def notEqual_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value1.type == Type.INT or value1.type == Type.DECIMAL:
            if value2.type == Type.INT or value2.type == Type.DECIMAL:
                return self.compare(value1.strValue, '!=', value2.strValue, c3dgen)
            env.setError("Los tipos no son válidos para operaciones relacionales (!=)", self.exp2.line, self.exp2.column)
            return ReturnC3D(isTmp = False, type = Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return self.compareStr(value1.strValue, '!=', value2.strValue, c3dgen)
        env.setError("Los tipos no son válidos para operaciones relacionales (!=)", self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def greatEqual_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return self.compare(value1.strValue, '>=', value2.strValue, c3dgen)
            env.setError("Los tipos no son válidos para operaciones relacionales (>=)", self.exp2.line, self.exp2.column)
            return ReturnC3D(isTmp = False, type = Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return self.compareStr(value1.strValue, '>=', value2.strValue, c3dgen)
        env.setError("Los tipos no son válidos para operaciones relacionales (>=)", self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def lessEqual_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return self.compare(value1.strValue, '<=', value2.strValue, c3dgen)
            env.setError("Los tipos no son válidos para operaciones relacionales (<=)", self.exp2.line, self.exp2.column)
            return ReturnC3D(isTmp = False, type = Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return self.compareStr(value1.strValue, '<=', value2.strValue, c3dgen)
        env.setError("Los tipos no son válidos para operaciones relacionales (<=)", self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def great_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return self.compare(value1.strValue, '>', value2.strValue, c3dgen)
            env.setError("Los tipos no son válidos para operaciones relacionales (>)", self.exp2.line, self.exp2.column)
            return ReturnC3D(isTmp = False, type = Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return self.compareStr(value1.strValue, '>', value2.strValue, c3dgen)
        env.setError("Los tipos no son válidos para operaciones relacionales (>)", self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def less_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value1.type in [Type.INT, Type.DECIMAL]:
            if value2.type in [Type.INT, Type.DECIMAL]:
                return self.compare(value1.strValue, '<', value2.strValue, c3dgen)
            env.setError("Los tipos no son válidos para operaciones relacionales (<)", self.exp2.line, self.exp2.column)
            return ReturnC3D(isTmp = False, type = Type.NULL)
        if value1.type in [Type.NVARCHAR, Type.NCHAR] and value2.type in [Type.NVARCHAR, Type.NCHAR]:
            return self.compareStr(value1.strValue, '<', value2.strValue, c3dgen)
        env.setError("Los tipos no son válidos para operaciones relacionales (<)", self.exp2.line, self.exp2.column)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def compare (self, value1: str, sign: str, value2: str, c3dgen: C3DGen) -> C3DGen:
        self.checkLbls(c3dgen)
        c3dgen.addIf(value1, sign, value2, self.trueLbl)
        c3dgen.addGoto(self.falseLbl)
        return ReturnC3D(isTmp = False, type = Type.BOOLEAN, trueLbl = self.trueLbl, falseLbl = self.falseLbl)

    def compareStr(self, value1: str, sign: str, value2: str, c3dgen: C3DGen) -> C3DGen:
        self.checkLbls(c3dgen)
        tmp1: str = c3dgen.newTmp()
        tmp2: str = c3dgen.newTmp()
        tmp3: str = c3dgen.newTmp()
        tmp4: str = c3dgen.newTmp()
        lbl1: str = c3dgen.newLbl()
        lbl2: str = c3dgen.newLbl()
        c3dgen.addAsign(tmp1, value1)
        c3dgen.addAsign(tmp2, value2)
        c3dgen.addLabel(lbl1)
        c3dgen.addGetHeap(tmp3, tmp1)
        c3dgen.addGetHeap(tmp4, tmp2)
        c3dgen.addIf(tmp3, '!=', tmp4, lbl2)
        c3dgen.addIf(tmp3, '==', '-1', lbl2)
        c3dgen.addExpression(tmp1, tmp1, '+', '1')
        c3dgen.addExpression(tmp2, tmp2, '+', '1')
        c3dgen.addGoto(lbl1)
        c3dgen.addLabel(lbl2)
        c3dgen.addIf(tmp3, sign, tmp4, self.trueLbl)
        c3dgen.addGoto(self.falseLbl)
        return ReturnC3D(isTmp = False, type = Type.BOOLEAN, trueLbl = self.trueLbl, falseLbl = self.falseLbl)

    def checkLbls(self, c3dgen: C3DGen) -> C3DGen:
        self.trueLbl = c3dgen.validLabel(self.trueLbl)
        self.falseLbl = c3dgen.validLabel(self.falseLbl)

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