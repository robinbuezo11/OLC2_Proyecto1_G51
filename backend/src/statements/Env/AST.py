class AST:
    def __init__(self):
        self.nodeID: int = 0

    def getNewID(self) -> int:
        self.nodeID += 1
        return self.nodeID

class ReturnAST:
    def __init__(self, dot: str, id: int):
        self.dot = dot
        self.id = id