from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.Type import ReturnType, Type
from utils.TypeInst import TypeInst

class Concatenar(Expression):
    def __init__(self, line: int, column: int, exp1: Expression, exp2: Expression):
        super().__init__(line, column, TypeInst.NATIVE_FUNC)
        self.exp1 = exp1
        self.exp2 = exp2

    def setField(self, field):
        pass

    def execute(self, env: Env) -> any:
        exp1 = self.exp1.execute(env)
        exp2 = self.exp2.execute(env)
        return ReturnType(exp1.value + exp2.value, Type.NVARCHAR)

    def ast(self, ast: AST) -> ReturnAST:
        pass