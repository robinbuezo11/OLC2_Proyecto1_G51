from statements.Abstracts.Instruction import Instruction
from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.TypeInst import TypeInst

class InsertTable(Instruction):
    def __init__(self, line: int, column: int, name: str, fields: list[str], values: list[Expression]):
        super().__init__(line, column, TypeInst.INSERT_TABLE)
        self.name = name
        self.fields = fields
        self.values = values

    def execute(self, env: Env) -> any:
        if len(self.fields) == len(self.values):
            env.insertTable(self.name, self.fields, self.values, self.line, self.column)
            return
        if len(self.fields) < len(self.values):
            env.setError('Inserta más valores de los esperados', self.line, self.column)
            return
        env.setError('Inserta menos valores de los esperados', self.line, self.column)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="INSERT"];'
        dot += f'\nnode_{id}_table[label="{self.name}"];'
        dot += f'\nnode_{id}_fields[label="FIELDS"];'
        for i in range(len(self.fields)):
            dot += f'\nnode_{id}_field_{i}[label="{self.fields[i]}"];'
            dot += f'\nnode_{id}_fields -> \nnode_{id}_field_{i};'
        dot += f'\nnode_{id}_values[label="VALORES"];'
        value: ReturnAST 
        for i in range(len(self.values)):
            value = self.values[i].ast(ast)
            dot += '\n' + value.dot
            dot += f'\nnode_{id}_values -> node_{value.id};'
        dot += f'\nnode_{id}_table -> node_{id}_fields;'
        dot += f'\nnode_{id}_table -> node_{id}_values;'
        dot += f'\nnode_{id} -> node_{id}_table'
        return ReturnAST(dot, id)