from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Env.Symbol import Symbol
from statements.Abstracts.Instruction import Instruction
from statements.Abstracts.Expression import Expression
from statements.Expressions.Primitive import Primitive
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type
from utils.TypeInst import TypeInst
from typing import Union, List

class InitID(Instruction):
    def __init__(self, line: int, column: int, id: Union[str, List[str]], type: Union[Type, List[Type]], value: Union[Expression, None]):
        super().__init__(line, column, TypeInst.INIT_ID)
        self.id = id
        self.type = type
        self.value = value

    def execute(self, env: Env) -> any:
        if type(self.id) == str and type(self.type) == Type and self.value:
            value: ReturnType = self.value.execute(env)
            if value.type == self.type or self.type == Type.DECIMAL and value.type == Type.INT or \
            self.type == Type.BIT and value.type == Type.INT and int(value.value) in [0, 1] or \
            self.type == Type.NCHAR and value.type == Type.NVARCHAR:
                env.saveID(self.id, value.value, self.type, self.line, self.column)
            else:
                env.setError('Los tipos no coinciden en la declaración', self.line, self.column)
        elif type(self.id) == list and type(self.type) == list and not self.value:
            for i in range(len(self.id)):
                env.saveID(self.id[i], 'NULL', self.type[i], self.line, self.column)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        c3dgen.addComment('------- Declaración -------')
        if type(self.id) == str and type(self.type) == Type and self.value:
            value: ReturnC3D = self.value.compile(env, c3dgen)
            if value.type == self.type or self.type == Type.DECIMAL and value.type == Type.INT or \
            self.type == Type.BIT and value.type == Type.INT and int(value.value) in [0, 1] or \
            self.type == Type.NCHAR and value.type == Type.NVARCHAR:
                self.init(self.id, value, env, c3dgen, currentType = self.type)
            else:
                env.setError('Los tipos no coinciden en la declaración', self.line, self.column)
        elif type(self.id) == list and type(self.type) == list and not self.value:
            for i in range(len(self.id)):
                self.init(self.id[i], ReturnC3D(type = self.type[i]), env, c3dgen, True)
        c3dgen.addComment("----- Fin Declaración -----")

    def init(self, id: str, value: ReturnC3D, env: Env, c3dgen: C3DGen, isNULL: bool = False, currentType: Type = Type.NULL):
        newId: Symbol = env.saveID_c3d(id, value.type, value.isTrue, self.line, self.column, currentType)
        tmp: str = str(env.size - 1)
        if not newId.isglobal:
            tmp = c3dgen.newTmp()
            c3dgen.addExpression(tmp, 'P', '+', newId.position)
        if not isNULL:
            c3dgen.addSetStack(tmp, value.strValue)
        else:
            newValue: ReturnC3D = Primitive(0, 0, 'NULL', Type.NVARCHAR).compile(env, c3dgen)
            c3dgen.addSetStack(tmp, newValue.strValue)

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="DECLARE"];'
        if type(self.id) == str and type(self.type) == Type and self.value:
            dot += f'\nnode_{id}_type[label="{self.getType(self.type)}"];'
            dot += f'\nnode_{id} -> node_{id}_type;'
            dot += f'\nnode_{id}_id[label="{self.id}"];'
            dot += f'\nnode_{id}_type -> node_{id}_id;'
            value : ReturnAST = self.value.ast(ast)
            dot += '\n'+value.dot
            dot += f'\nnode_{id}_type -> node_{value.id};'
        elif type(self.id) == list and type(self.type) == list and not self.value:
            for i in range(len(self.id)):
                dot += f'\nnode_{id}_type_{i}[label="{self.getType(self.type[i])}"];'
                dot += f'\nnode_{id} -> node_{id}_type_{i};'
                dot += f'\nnode_{id}_id_{i}[label="${self.id[i]}"];'
                dot += f'\nnode_{id}_type_{i} -> node_{id}_id_{i};'
        return ReturnAST(dot, id)

    def getType(self, type: Type) -> str:
        match type:
            case Type.INT:
                return "INT"
            case Type.DECIMAL:
                return "DECIMAL"
            case Type.NCHAR:
                return "NCHAR"
            case Type.NVARCHAR:
                return "NVARCHAR"
            case Type.DECIMAL:
                return "BOOLEAN"
            case Type.DATE:
                return "DATE"
            case Type.TABLE:
                return "TABLE"
            case _:
                return "NULL"