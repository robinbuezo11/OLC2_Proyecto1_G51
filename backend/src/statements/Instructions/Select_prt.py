from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.TypeInst import TypeInst
from utils.Type import ReturnType

class Select_prt(Instruction):
    def __init__(self, line: int, column: int, expression: list[list[any]]):
        super().__init__(line, column, TypeInst.SELECT)
        self.expression = expression

    def execute(self, env: Env) -> any:
        value: ReturnType
        for i in range(len(self.expression)):
            value = self.expression[i][0].execute(env) if self.expression[i] else None
            if value:
                if self.expression[i][1] != '':
                    env.setPrint(self.expression[i][1] + ': ' + str(value.value))
                else:
                    env.setPrint(value.value)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="SELECT"];'
        value: ReturnAST
        for i in range(len(self.expression)):
            value = self.expression[i][0].ast(ast)
            if self.expression[i][1] != '':
                dot += f'\nnode_{id}_AS{i}[label="AS"];'
                dot += f'\nnode_{id} -> node_{id}_AS{i};'
                dot += f'\n{value.dot}'
                dot += f'\nnode_{id}_AS{i} -> node_{value.id};'
                dot += f'\nnode_{id}_ASTXT{i}[label="{self.expression[i][1]}"];'
                dot += f'\nnode_{id}_AS{i} -> node_{id}_ASTXT{i};'
            else:
                dot += f'\n{value.dot}'
                dot += f'\nnode_{id} -> node_{value.id};'
        return ReturnAST(dot, id)