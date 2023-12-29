from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class SetHeap(Instruction):
    def __init__(self, index: str, value: str):
        super().__init__(Type.SETSTACK)
        self.index = index
        self.value = value

    def __str__(self) -> str:
        return f'\theap[(int) {self.index} ] = {self.value};'