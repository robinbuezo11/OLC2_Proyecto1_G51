from utils.Outs import printConsole, errors
from utils.Type import Type, ReturnType
from utils.Error import Error
from utils.TypeError import TypeError
from statements.Env.Symbol import Symbol
from statements.Abstracts.Expression import Expression


class Env:
    def __init__(self, previous: 'Env' or None, name: str):
        self.ids: dict[str, Symbol] = {}
        self.functions: dict[str, any] = {}
        self.tables: dict[str, any] = {}
        self.previous = previous
        self.name = name

    def saveID(self, id: str, value: any, type: Type, line: int, column: int):
        env: Env = self
        if id.lower() not in env.ids:
            env.ids[id.lower()] = Symbol(value, id.lower(), type)
        else:
            self.setError('Redeclaración de variable existente', line, column)

    def getValue(self, id: str) -> Symbol:
        env: Env = self
        while env:
            if id.lower() in env.ids:
                return env.ids.get(id.lower())
            env = env.previous
        return None

    def reasignID(self, id: str, value: ReturnType, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.ids:
                symbol: Symbol = env.ids.get(id.lower())
                if value.type == symbol.type or symbol.type == Type.DECIMAL and value.type == Type.INT or \
                symbol.type == Type.BIT and value.type == Type.INT and int(value.value) in [0, 1] or \
                symbol.type == Type.NCHAR and value.type == Type.NVARCHAR:
                    symbol.value = value.value
                    env.ids[id.lower()] = symbol
                    return True
                env.setError(f'Los tipos no coinciden en la asignación. Intenta asignar un "{env.getTypeOf(value.type)}" a un "{env.getTypeOf(symbol.type)}"', line, column)
                return False
            env = env.previous
        self.setError('Resignación de valor a variable inexistente', line, column)
        return False

    def setPrint(self, print_: str):
        printConsole.append(str(print_))

    def setError(self, errorD: str, line: int, column: int):
        if not self.match(errorD, line, column + 1):
            errors.append(Error(line, column + 1, TypeError.SEMANTIC, errorD))

    def match(self, err: str, line: int, column: int):
        for error in errors:
            if(error.__str__() == (Error(line, column, TypeError.SEMANTIC, err)).__str__()):
                return True
        return False

    def getTypeOf(self, type: Type) -> str:
        match type:
            case Type.INT:
                return "INT"
            case Type.DECIMAL:
                return "DECIMAL"
            case Type.NCHAR:
                return "NCHAR"
            case Type.NVARCHAR:
                return "NVARCHAR"
            case Type.BIT:
                return "BIT"
            case Type.DATE:
                return "DATE"
            case Type.TABLE:
                return "TABLE"
            case _:
                return "NULL"