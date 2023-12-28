from C3D.Instruction import Instruction
from C3D.Type import Type

class Goto(Instruction):
    def __init__(self, lbl: str):
        super().__init__(Type.GOTO)
        self.lbl = lbl

    def __str__(self) -> str:
        return '\tgoto ' + self.lbl + ';'