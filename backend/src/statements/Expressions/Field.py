from utils.TypeExp import TypeExp
from statements.Env.AST import AST, ReturnAST
from statements.Abstracts.Expression import Expression
from statements.Env.Env import Env
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class Field(Expression):
    def __init__(self, line: int, column: int, id: str):
        super().__init__(line, column, TypeExp.FIELD)
        self.id = id
        self.field: dict[str, any] = {}
        self.isFieldName: bool = False

    def setIsFieldName(self, isFieldName: bool):
        self.isFieldName = isFieldName

    def setField(self, field: dict[str, any]) -> any:
        self.field = field

    def execute(self, env: Env) -> ReturnType:
        if not self.isFieldName:
            if self.id.lower() in self.field:
                return self.field[self.id.lower()].values[0].getData()
            env.setError(f'No existe el campo {self.id.lower()}', self.line, self.column)
            return ReturnType('NULL', Type.NULL)
        return ReturnType(self.id, Type.NULL)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="{self.id}"];'
        return ReturnAST(dot, id)