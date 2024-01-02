from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Objects.Table import Field
from statements.Abstracts.Expression import Expression
from statements.Env.Symbol import Symbol
from utils.TypeExp import TypeExp
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class AccessID(Expression):
    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column, TypeExp.ACCESS_ID)
        self.id = id

    def setField(self, _: dict[str, Field]):
        pass

    def execute(self, env: Env) -> ReturnType:
        value: Symbol | None = env.getValue(self.id, self.line, self.column)
        if value:
            return ReturnType(value.value, value.type)
        return ReturnType('NULL', Type.NULL)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        c3dgen.addComment('--------- Acceso ----------')
        value: Symbol = env.getValue(self.id, self.line, self.column)
        if value:
            tmp1: str
            tmp2: str = str(value.position)
            if not value.isglobal:
                tmp2 = c3dgen.newTmp()
                tmp1 = c3dgen.newTmp()
                c3dgen.addExpression(tmp2, 'P', '+', value.position)
            else:
                tmp1 = c3dgen.newTmp()
            c3dgen.addGetStack(tmp1, tmp2)
            c3dgen.addComment('------- Fin Acceso --------')
            return ReturnC3D(isTmp = True, strValue = tmp1, type = value.currentType)
        c3dgen.addComment('------- Fin Acceso --------')

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.id}"];'
        return ReturnAST(dot, id)