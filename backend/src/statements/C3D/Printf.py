from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Printf(Instruction):
    def __init__(self, type: str, value: str):
        super().__init__(Type.PRINTF)
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f'\tprintf(\"%{self.type}\", {self.value});'