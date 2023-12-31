from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Objects.Table import Field
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type
from utils.TypeExp import TypeExp

class Primitive(Expression):
    def __init__(self, line: int, column: int, value: any, type: Type):
        super().__init__(line, column, TypeExp.PRIMITIVE)
        self.value = value
        self.type = type

    def setField(self, _: dict[str, Field]) -> any:
        pass

    def execute(self, _: Env) -> ReturnType:
        match self.type:
            case Type.INT:
                return ReturnType(int(self.value), self.type)
            case Type.DECIMAL:
                return ReturnType(float(self.value), self.type)
            case Type.DATE:
                return ReturnType(str(self.value), self.type)
            case Type.DATETIME:
                return ReturnType(str(self.value), self.type)
            case _:
                self.value = self.value.replace('\\n', '\n')
                self.value = self.value.replace('\\t', '\t')
                self.value = self.value.replace('\\"', '\"')
                self.value = self.value.replace("\\'", '\'')
                self.value = self.value.replace('\\\\', '\\')
                return ReturnType(self.value, self.type)

    def compile(self, _: Env, c3dgen: C3DGen) -> ReturnC3D:
        match self.type:
            case Type.INT:
                return ReturnC3D(isTmp = False, strValue = str(self.value), type = self.type)
            case Type.DECIMAL:
                return ReturnC3D(isTmp = False, strValue = str(self.value), type = self.type)
            case _:
                self.value = self.value.replace('\\n', '\n')
                self.value = self.value.replace('\\t', '\t')
                self.value = self.value.replace('\\"', '\"')
                self.value = self.value.replace("\\'", '\'')
                self.value = self.value.replace('\\\\', '\\')
                tmp = c3dgen.newTmp()
                c3dgen.addAsign(tmp, 'H')
                for ascii in self.value:
                    c3dgen.addSetHeap('H', ord(ascii))
                    c3dgen.nextHeap()
                c3dgen.addSetHeap('H', '-1')
                c3dgen.nextHeap()
                return ReturnC3D(isTmp = True, strValue = tmp, type = self.type)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.value}"];'
        return ReturnAST(dot, id)