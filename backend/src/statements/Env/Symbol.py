from utils.Type import Type

class Symbol:
    def __init__(self, value: any, id: str, type: Type):
        self.value = value
        self.id = id.lower()
        self.type = type

    def __str__(self) -> str:
        return f'{self.id}: {self.type} = {self.value}'