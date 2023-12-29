from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class Function(Instruction):
    def __init__(self, id: str):
        super().__init__(Type.FUNCTION)
        self.id = id

    def __str__(self) -> str:
        return 'void ' + self.id + '() {'