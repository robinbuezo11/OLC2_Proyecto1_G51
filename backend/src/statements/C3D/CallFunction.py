from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class CallFunction(Instruction):
    def __init__(self, id: str):
        super().__init__(Type.CALLFUNCTION)
        self.id = id

    def __str__(self) -> str:
        return f'\t' + self.id + '();'