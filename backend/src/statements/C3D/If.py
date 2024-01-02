from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class If(Instruction):
    def __init__(self, left: str, operator: str, right: str, lbl: str):
        super().__init__(Type.IF)
        self.left = str(left)
        self.operator = str(operator)
        self.right = str(right)
        self.lbl = str(lbl)

    def __str__(self) -> str:
        return f'\tif({self.left} {self.operator} {self.right}) goto {self.lbl};'