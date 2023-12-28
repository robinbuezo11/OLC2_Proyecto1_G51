from C3D.Instruction import Instruction
from C3D.Type import Type

class End(Instruction):
    def __init__(self):
        super().__init__(Type.END)

    def __str__(self) -> str:
        return '}\n'