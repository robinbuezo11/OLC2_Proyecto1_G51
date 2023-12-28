from C3D.Instruction import Instruction
from C3D.Type import Type

class Label(Instruction):
    def __init__(self, lbl: str):
        super().__init__(Type.LABEL)
        self.lbl = lbl

    def __str__(self) -> str:
        return self.lbl + ':'