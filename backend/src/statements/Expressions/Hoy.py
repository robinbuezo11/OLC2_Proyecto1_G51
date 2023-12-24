from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.Type import ReturnType, Type
from utils.TypeInst import TypeInst
from datetime import datetime

class Hoy(Expression):
    def __init__(self, line: int, column: int):
        super().__init__(line, column, TypeInst.NATIVE_FUNC)

    def setField(self, field):
        pass

    def execute(self, _: Env) -> any:
        dateT = datetime.now()
        f = "%d-%m-%Y %H:%M"
        return ReturnType(dateT.strftime(f), Type.NVARCHAR)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="HOY"];'
        return ReturnAST(dot, id)