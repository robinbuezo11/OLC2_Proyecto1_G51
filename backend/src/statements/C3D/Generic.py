from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Generic(Instruction):
    def __init__(self, arg: str):
        super().__init__(Type.GENERIC)
        self.arg = str(arg)

    def __str__(self) -> str:
        return self.arg