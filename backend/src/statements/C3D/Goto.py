from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Goto(Instruction):
    def __init__(self, lbl: str):
        super().__init__(Type.GOTO)
        self.lbl = str(lbl)

    def __str__(self) -> str:
        return '\tgoto ' + self.lbl + ';'