from utils.Type import Type

class Attribute:
    def __init__(self, line: int, column: int, id: str, type: Type, length: int, props: dict[str, bool] = {'notNull': False, 'primaryKey': False, 'foreignKey': False }):
        self.line = line
        self.column = column
        self.id = id
        self.type = type
        self.length = length
        self.props = props

    def toString(self) -> str:
        return f'{self.id} {self.type}({self.length}) {self.props}'