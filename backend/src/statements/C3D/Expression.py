from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Expression(Instruction):
    def __init__(self, target: str, left: str, operator: str, right: str):
        super().__init__(Type.EXPRESSION)
        self.target = str(target)
        self.left = str(left)
        self.operator = str(operator)
        self.right = str(right)

    def __str__(self) -> str:
        return f'\t{self.target} = {self.left} {self.operator} {self.right};'