from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.TypeInst import TypeInst

class DropTable(Instruction):
    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column, TypeInst.DELETE_TABLE)
        self.id = id

    def execute(self, env: Env) -> any:
        env.dropTable(self.id, self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="DROP"];'
        dot += f'\nnode_{id}_drop[label="{self.id}"]'
        dot += f'\nnode_{id} -> node_{id}_drop;'
        return ReturnAST(dot, id)