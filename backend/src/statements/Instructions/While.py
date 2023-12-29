from statements.Abstracts.Instruction import Instruction
from statements.Abstracts.Expression import Expression
from utils.TypeInst import TypeInst
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env


class While(Instruction):
    def __init__(self, line: int, column: int, condition: Expression, block: Instruction):
        super().__init__(line, column, TypeInst.LOOP_WHILE)
        self.condition = condition
        self.block = block

    def execute(self, env: Env) -> any:
        whileEnv: Env = Env(env, f'{env.name} while')
        condition: ReturnType = self.condition.execute(whileEnv)
        while condition.value:
            block: ReturnType = self.block.execute(whileEnv)
            if block:
                if block.value == TypeInst.CONTINUE:
                    condition = self.condition.execute(whileEnv)
                    continue
                elif block.value == TypeInst.BREAK:
                    break
                return block
            condition = self.condition.execute(whileEnv)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="WHILE"];'
        dot += f'\nnode_{id}_cond[label="CONDICION"]'
        cond: ReturnAST = self.condition.ast(ast)
        dot += '\n' + cond.dot
        dot += f'\nnode_{id}_cond -> node_{cond.id};'
        inst: ReturnAST = self.block.ast(ast)
        dot += '\n' + inst.dot
        dot += f'\nnode_{id} -> node_{inst.id};'
        dot += f'\nnode_{id} -> node_{id}_cond;'
        return ReturnAST(dot, id)