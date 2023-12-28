from C3D.Instruction import Instruction
from C3D.Type import Type

class GetHeap(Instruction):
    def __init__(self, target: str, index: str):
        super().__init__(Type.GETHEAP)
        self.target = target
        self.index = index

    def __str__(self) -> str:
        return '\t' + self.target + ' = heap[int(int) ' + self.index + '];'