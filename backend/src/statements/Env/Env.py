from utils.Outs import printConsole, errors
from utils.Type import Type, ReturnType
from utils.Error import Error
from utils.TypeError import TypeError
from Env.Symbol import Symbol
from Abstracts.Expression import Expression


class Env:
    def __init__(self, previous: 'Env' or None, name: str):
        self.ids: dict[str, Symbol] = {}
        self.functions: dict[str, any] = {}
        self.tables: dict[str, any] = {}
        self.previous = previous
        self.name = name