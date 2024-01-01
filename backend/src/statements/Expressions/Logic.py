from statements.Objects.Table import Field
from utils.TypeExp import TypeExp
from statements.Env.AST import AST, ReturnAST
from statements.Abstracts.Expression import Expression
from statements.Env.Env import Env
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class Logic(Expression):
    def __init__(self, line: int, column: int, exp1: Expression, sign: str, exp2: Expression):
        super().__init__(line, column, TypeExp.NATIVE_FUNC)
        self.exp1 = exp1
        self.sign = sign
        self.exp2 = exp2

    def setField(self, field: dict[str, Field]) -> any:
        if self.exp1:
            self.exp1.setField(field)
        self.exp2.setField(field)

    def execute(self, env: Env) -> ReturnType:
        match self.sign.upper():
            case '&&':
                return self.and_(env)
            case '||':
                return self.or_(env)
            case '!':
                return self.not_(env)
            case _:
                return ReturnType('NULL', Type.NULL)

    def and_(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = Type.BOOLEAN
        return ReturnType(value1.value and value2.value, self.type)

    def or_(self, env: Env) -> ReturnType:
        value1: ReturnType = self.exp1.execute(env)
        value2: ReturnType = self.exp2.execute(env)
        self.type = Type.BOOLEAN
        return ReturnType(value1.value or value2.value, self.type)

    def not_(self, env: Env) -> ReturnType:
        value: ReturnType = self.exp2.execute(env)
        self.type = Type.BOOLEAN
        return ReturnType(not value.value, self.type)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        match self.sign.upper():
            case '&&':
                return self.and_c3d(env, c3dgen)
            case '||':
                return self.or_c3d(env, c3dgen)
            case '!':
                return self.not_c3d(env, c3dgen)
            case _:
                return ReturnC3D(isTmp = False, type = Type.NULL)

    def and_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        andLbl: str
        self.checkLbls(c3dgen)
        andLbl = self.exp1.trueLbl = c3dgen.newLbl()
        self.exp2.trueLbl = self.trueLbl
        self.exp1.falseLbl = self.exp2.falseLbl = self.falseLbl
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        self.type = Type.BOOLEAN
        if value1.type != Type.BOOLEAN:
            return ReturnC3D(isTmp = False, type = Type.NULL)
        c3dgen.addLabel(andLbl)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value2.type == Type.BOOLEAN:
            return ReturnC3D(isTmp = True, type = Type.BOOLEAN, trueLbl = self.trueLbl, falseLbl = self.falseLbl)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def or_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        orLbl: str
        self.checkLbls(c3dgen)
        orLbl = self.exp1.falseLbl = c3dgen.newLbl()
        self.exp2.falseLbl = self.falseLbl
        self.exp1.trueLbl = self.exp2.trueLbl = self.trueLbl
        value1: ReturnC3D = self.exp1.compile(env, c3dgen)
        if value1.type != Type.BOOLEAN:
            return ReturnC3D(isTmp = False, type = Type.NULL)
        c3dgen.addLabel(orLbl)
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value2.type == Type.BOOLEAN:
            return ReturnC3D(isTmp = True, type = Type.BOOLEAN, trueLbl = self.trueLbl, falseLbl = self.falseLbl)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def not_c3d(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        self.checkLbls(c3dgen)
        self.exp2.falseLbl = self.trueLbl
        self.exp2.trueLbl = self.falseLbl
        value2: ReturnC3D = self.exp2.compile(env, c3dgen)
        if value2.type == Type.BOOLEAN:
            return ReturnC3D(isTmp = True, type = Type.BOOLEAN, trueLbl = self.trueLbl, falseLbl = self.falseLbl)
        return ReturnC3D(isTmp = False, type = Type.NULL)

    def checkLbls(self, c3dgen: C3DGen):
        self.trueLbl = c3dgen.validLabel(self.trueLbl)
        self.falseLbl = c3dgen.validLabel(self.falseLbl)

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