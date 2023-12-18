from statements.Abstracts.Instruction import Instruction
from statements.Env.Env import Env
from utils.TypeInst import TypeInst
from utils.Type import Type
from statements.Expressions.Parameter import Parameter
from statements.Env.AST import AST, ReturnAST

class Function(Instruction):
    def __init__(self, line: int, column: int, id: str, parameters: list[Parameter], block: Instruction, type: Type):
        super().__init__(line, column, TypeInst.INIT_FUNCTION)
        self.id = id
        self.parameters = parameters
        self.block = block
        self.type = type

    def execute(self, env: Env) -> any:
        env.saveFunction(self.id, self)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="FUNCTION"];'
        dot += f'\nnode_{id}_name[label="{self.id}"];'
        dot += f'\nnode_{id} -> node_{id}_name;'
        if len(self.parameters) > 0:
            dot += f'\nnode_{id}_params[label="PARAMS"];'
            for i in range(len(self.parameters)):
                dot += f'\nnode_{id}_param_{i}[label="{self.parameters[i].id}"];'
                dot += f'\nnode_{id}_params -> node_{id}_param_{i};'
            dot += f'\nnode_{id}_name -> node_{id}_params;'
        inst: ReturnAST = self.block.ast(ast)
        dot += '\n' + inst.dot
        dot += f'\nnode_{id}_name -> node_{inst.id};'
        return ReturnAST(dot, id)