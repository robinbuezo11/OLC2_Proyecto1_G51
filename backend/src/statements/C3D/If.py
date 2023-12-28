from C3D.Instruction import Instruction
from C3D.Type import Type

class If(Instruction):
    def __init__(self, left: str, operator: str, right: str, lbl: str):
        super().__init__(Type.IF)
        self.laft = left
        self.operator = operator
        self.right = right
        self.lbl = lbl

    def __str__(self) -> str:
        return f'\tif({self.left} {self.operator} {self.right}) goto {self.lbl};'