from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Label(Instruction):
    def __init__(self, lbl: str):
        super().__init__(Type.LABEL)
        self.lbl = str(lbl)

    def __str__(self) -> str:
        return self.lbl + ':'