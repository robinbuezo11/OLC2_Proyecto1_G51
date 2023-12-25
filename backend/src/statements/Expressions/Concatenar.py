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
        id = ast.getNewID()
        dot = f'node_{id}[label="CONCATENAR"];'
        value1: ReturnAST = self.exp1.ast(ast)
        dot += '\n' + value1.dot
        value2: ReturnAST = self.exp2.ast(ast)
        dot += '\n' + value2.dot
        dot += f'\nnode_{id} -> node_{value1.id};'
        dot += f'\nnode_{id} -> node_{value2.id};'
        return {dot: dot, id: id}