from C3D.Instruction import Instruction
from C3D.Type import Type

class Return(Instruction):
    def __init__(self):
        super().__init__(Type.RETURN)

    def __str__(self) -> str:
        return '\treturn;'