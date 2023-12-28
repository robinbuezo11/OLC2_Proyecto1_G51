from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class GetStack(Instruction):
    def __init__(self, target: str, index: str):
        super().__init__(Type.GETSTACK)
        self.target = target
        self.index = index

    def __str__(self) -> str:
        return '\t' + self.target + ' = stack[(int) ' + str(self.index) + '];'