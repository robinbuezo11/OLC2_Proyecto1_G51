from statements.Abstracts.Instruction import Instruction
from utils.TypeInst import TypeInst
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnC3D, Type

class TruncateTable(Instruction):
    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column, TypeInst.TRUNCATE_TABLE)
        self.id = id

    def execute(self, env: Env) -> any:
        env.truncateTable(self.id, self.line, self.column)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="TRUNCATE"];'
        dot += f'\nnode_{id}_truncate[label="{self.id}"]'
        dot += f'\nnode_{id} -> node_{id}_truncate;'
        return ReturnAST(dot, id)