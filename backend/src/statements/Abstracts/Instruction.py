from abc import ABC, abstractmethod
from utils.TypeInst import TypeInst
from statements.Env.Env import Env
from statements.Env.AST import AST, ReturnAST
from statements.C3D.C3DGen import C3DGen

class Instruction(ABC):
    def __init__(self, line: int, column: int, typeInst: TypeInst):
        self.line = line
        self.column = column
        self.typeInst = typeInst

    @abstractmethod
    def execute(self, env: Env, c3dgen: C3DGen) -> any:
        pass

    @abstractmethod
    def ast(self, ast: AST) -> ReturnAST:
        pass