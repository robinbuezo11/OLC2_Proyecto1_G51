from utils.Type import Type

class Parameter:
    def __init__(self, line: int, column: int, id: str, type: Type):
        self.line = line
        self.column = column
        self.id = id
        self.type = type