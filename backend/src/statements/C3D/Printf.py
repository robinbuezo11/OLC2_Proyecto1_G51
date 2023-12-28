from C3D.Instruction import Instruction
from C3D.Type import Type

class Printf(Instruction):
    def __init__(self, type: str, value: str):
        super().__init__(Type.PRINTF)
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return '\tprintf(\"%' + self.type + '\", ' + self.value + ');'