from abc import ABC, abstractmethod
from utils.TypeExp import TypeExp

class Expression(ABC):
    def __init__(self, line: int, column: int, typeExp: TypeExp):
        self.line = line
        self.column = column
        self.typeExp = typeExp
        self.trueLabel = ''
        self.falseLabel = ''

    @abstractmethod
    def setField(self, field):
        pass

    @abstractmethod
    def execute(self, env):
        pass

    @abstractmethod
    def compile(self, env, c3dgen):
        pass

    @abstractmethod
    def ast(self, ast):
        pass