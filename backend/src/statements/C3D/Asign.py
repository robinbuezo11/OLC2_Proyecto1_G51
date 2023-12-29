from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Asign(Instruction):
    def __init__(self, target: str, value: str):
        super().__init__(Type.ASIGN)
        self.target = target
        self.value = value

    def __str__(self) -> str:
        return f'\t{self.target} = {self.value};'