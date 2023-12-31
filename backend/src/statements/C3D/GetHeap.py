from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type

class GetHeap(Instruction):
    def __init__(self, target: str, index: str):
        super().__init__(Type.GETHEAP)
        self.target = str(target)
        self.index = str(index)

    def __str__(self) -> str:
        return f'\t{self.target} = heap[(int) {self.index}];'