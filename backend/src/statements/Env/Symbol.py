from utils.Type import Type

class Symbol:
    def __init__(self, value: any, id: str, type: Type, position: int = None, isGlobal: bool = None, isTrue: bool = None, currentType: Type = Type.NULL):
        self.value = value
        self.id = id.lower()
        self.type = type
        self.position = position
        self.isglobal = isGlobal
        self.isTrue = isTrue
        self.currentType = currentType

    def __str__(self) -> str:
        return f'{self.id}: {self.type} = {self.value}'