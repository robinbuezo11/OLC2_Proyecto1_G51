from C3D.Instruction import Instruction
from C3D.Type import Type

class Generic(Instruction):
    def __init__(self, arg: str):
        super().__init__(Type.GENERIC)
        self.arg = arg

    def __str__(self) -> str:
        return self.arg