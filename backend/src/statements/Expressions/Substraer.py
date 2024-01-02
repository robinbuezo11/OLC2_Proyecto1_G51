from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type
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
                env.setError("Los tipos no son válidos para operaciones relacionales (<)", self.exp2.line, self.exp2.column)
                return ReturnType('NULL', Type.NULL)
            # error
            return ReturnType('NULL', Type.NULL)
        # error
        return ReturnType('NULL', Type.NULL)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="SUBSTRAER"];'
        string: ReturnAST = self.string.ast(ast)
        dot += '\n' + string.dot
        value1: ReturnAST = self.exp1.ast(ast)
        dot += '\n' + value1.dot
        value2: ReturnAST = self.exp2.ast(ast)
        dot += '\n' + value2.dot
        dot += f'\nnode_{id} -> node_{string.id};'
        dot += f'\nnode_{id} -> node_{value1.id};'
        dot += f'\nnode_{id} -> node_{value2.id};'
        return ReturnAST(dot, id)