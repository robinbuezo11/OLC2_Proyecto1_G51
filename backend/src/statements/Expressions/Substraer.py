from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.Type import ReturnType, Type
from utils.TypeInst import TypeInst

class Substraer(Expression):
    def __init__(self, line: int, column: int, string: Expression, exp1: Expression, exp2: Expression):
        super().__init__(line, column, TypeInst.NATIVE_FUNC)
        self.string = string
        self.exp1 = exp1
        self.exp2 = exp2

    def setField(self, field):
        pass

    def execute(self, env: Env) -> any:
        string: ReturnType = self.string.execute(env)
        exp1: ReturnType = self.exp1.execute(env)
        exp2: ReturnType = self.exp2.execute(env)
        if string.type in [Type.NVARCHAR, Type.NCHAR]:
            if exp1.type == Type.INT:
                if exp2.type == Type.INT:
                    return ReturnType(string.value[exp1.value - 1:exp2.value], Type.NVARCHAR)
                #error
                return ReturnType('NULL', Type.NULL)
            # error
            return ReturnType('NULL', Type.NULL)
        # error
        return ReturnType('NULL', Type.NULL)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="Substraer"];'
        return ReturnAST(dot, id)