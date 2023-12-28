from C3D.Instruction import Instruction
from C3D.Type import Type

class Expression(Instruction):
    def __init__(self, target: str, left: str, operator: str, right: str):
        super().__init__(Type.EXPRESSION)
        self.target = target
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return '\t' + self.target + ' = ' + self.left + ' ' + self.right + ';'