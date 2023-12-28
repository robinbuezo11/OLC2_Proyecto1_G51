from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Abstracts.Instruction import Instruction
from statements.Abstracts.Expression import Expression
from utils.TypeInst import TypeInst
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnC3D, Type

class AsignID(Instruction):
    def __init__(self, line: int, column: int, id: str, value: Expression):
        super().__init__(line, column, TypeInst.ASIGN_ID)
        self.id = id
        self.value = value

    def execute(self, env: Env):
        value = self.value.execute(env)
        env.reasignID(self.id, value, self.line, self.column)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="SET"];'
        value1: ReturnAST = self.value.ast(ast)
        dot += f'\nnode_{id}_id[label="{self.id}"]'
        dot += f'\nnode_{id} -> node_{id}_id'
        dot += '\n' + value1.dot
        dot += f'\nnode_{id} -> node_{value1.id};'
        return ReturnAST(dot, id)