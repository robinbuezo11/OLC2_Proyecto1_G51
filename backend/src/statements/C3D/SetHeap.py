from C3D.Instruction import Instruction
from C3D.Type import Type

class SetHeap(Instruction):
    def __init__(self, index: str, value: str):
        super().__init__(Type.SETSTACK)
        self.index = index
        self.value = value

    def __str__(self) -> str:
        return '\theap[(int) ' + self.index + '] = ' + self.value + ';'