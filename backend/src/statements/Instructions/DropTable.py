from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.TypeInst import TypeInst
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnC3D, Type

class DropTable(Instruction):
    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column, TypeInst.DELETE_TABLE)
        self.id = id

    def execute(self, env: Env) -> any:
        env.dropTable(self.id, self.line, self.column)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="DROP"];'
        dot += f'\nnode_{id}_drop[label="{self.id}"]'
        dot += f'\nnode_{id} -> node_{id}_drop;'
        return ReturnAST(dot, id)