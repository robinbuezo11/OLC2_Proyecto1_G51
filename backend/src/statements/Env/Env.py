from utils.Outs import printConsole, errors
from utils.Type import Type, ReturnType
from utils.Error import Error
from utils.TypeError import TypeError
from statements.Env.Symbol import Symbol
from statements.Abstracts.Expression import Expression
from utils.Global import *


class Env:
    def __init__(self, previous: 'Env' or None, name: str):
        self.ids: dict[str, Symbol] = {}
        self.functions: dict[str, any] = {}
        self.tables: dict[str, any] = {}
        self.previous = previous
        self.name = name

    # === VARIABLES ===
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

    # === FUNCTIONS ===
    def saveFunction(self, id: str, func: any):
        env: Env = self
        if not id.lower() in env.functions:
            env.functions[id.lower()] = func
        else:
            self.setError('Redefinición de función existente', func.line, func.column)

    def getFunction(self, id: str) -> any:
        env: Env = self
        while env:
            if id.lower() in env.functions:
                return env.functions.get(id.lower())
            env = env.previous
        return None

    # === TABLES ===
    def saveTable(self, id: str, table: any, line: int, column: int):
        env: Env = self
        if not id.lower() in env.tables:
            env.tables[id.lower()] = table
            self.setPrint(f'Tabla \'{id.lower()}\' creada. {line}:{column + 1}')
        else:
            self.setError('Redefinición de tabla existente', line, column)

    def insertTable(self, id: str, fields: list[str], values: list[Expression], line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                if env.tables.get(id.lower()).validateFields(fields):
                    newRow: dict[str, list[any]] = env.tables.get(id.lower()).getFieldsRow()
                    result: ReturnType
                    dataXml = []
                    for i in range(len(fields)):
                        result = values[i].execute(self)
                        newRow[fields[i].lower()] = [result.type, result.value]
                        dataXml.append({"value": result.value, "column": fields[i].lower()})
                    if env.tables.get(id.lower()).insert(env, newRow, line, column):
                        res = xml.insert(getUsedDatabase(), id.lower(), dataXml)
                        if not res[0]:
                            self.setPrint(res[1])
                            return False
                        self.setPrint(f'Registro insertado exitosamente en Tabla \'{id.lower()}\'. {line}:{column + 1}')
                        return True
                    return False
                self.setError(f'Inserta dato en columna inexistente en Tabla \'{id.lower()}\'', line, column)
                return False
            env = env.previous
        self.setError('Insertar en tabla inexistente', line, column)
        return False

    def truncateTable(self, id: str, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                env.tables.get(id.lower()).truncate()
                self.setPrint(f'Registros eliminados de Tabla \'{id.lower()}\'. {line}:{column + 1}')
                return True
            env = env.previous
        self.setError('Truncar tabla inexistente', line, column)
        return False

    def dropTable(self, id: str, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                del env.tables[id.lower()]
                self.setPrint(f'Tabla \'{id.lower()}\' eliminada. {line}:{column + 1}')
                return True
            env = env.previous
        self.setError('Eliminación de tabla inexistente', line, column)
        return False

    def deleteTable(self, id: str, condition: Expression, line: int, column: int):
        env: Env = self
        while env:
            if id.lower() in env.tables:
                env.tables.get(id.lower()).deleteWhere(condition, self)
                self.setPrint(f'Eliminación de Tabla \'{id.lower()}\'. {line}:{column + 1}')
                return
            env = env.previous
        self.setError('Eliminar registro en tabla inexistente', line, column)
        return False

    def updateTable(self, id: str, fields: list[str], values: list[Expression], condition: Expression, line: int, column: int):
        env: Env = self
        while env:
            if id.lower() in env.tables:
                env.tables.get(id.lower()).updateWhere(condition, fields, values, self)
                self.setPrint(f'Tabla \'{id.lower()}\' actualizada. {line}:{column + 1}')
                return True
            env = env.previous
        self.setError('Actualizar registro en tabla inexistente', line, column)
        return False

    def selectTable(self, id: str, fields: list[list[any]] or str, condition: Expression, line: int, column: int):
        env: Env = self
        while env:
            if id.lower() in env.tables:
                table = env.tables.get(id.lower()).select(fields, condition, self)
                self.setPrint(f'Selección en Tabla \'{id.lower()}\'. {line}:{column + 1}')
                env.selectPrint(table if table else [])
                return True
            env = env.previous
        self.setError('Selección en tabla inexistente', line, column)
        return False

    def addColumn(self, id: str, newColumn: str, type: Type, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                if not newColumn.lower() in env.tables.get(id.lower()).fields:
                    env.tables.get(id.lower()).addColumn(newColumn, type)
                    self.setPrint(f'Columna {newColumn.lower()} insertada exitosamente en Tabla \'{id.lower()}\'. {line}:{column + 1}')
                    return True
                self.setError(f'Ya hay una columna {newColumn.lower()} en Tabla \'{id.lower()}\'', line, column)
                return False
            env = env.previous
        self.setError('Alterar tabla inexistente', line, column)
        return False

    def dropColumn(self, id: str, dropColumn: str, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                if dropColumn.lower() in env.tables.get(id.lower()).fields:
                    env.tables.get(id.lower()).dropColumn(dropColumn)
                    self.setPrint(f'Columna {dropColumn.lower()} eliminada exitosamente de la Tabla \'{id.lower()}\'. {line}:{column + 1}')
                    return True
                self.setError(f'La columna {dropColumn.lower()} no existe en Tabla \'{id.lower()}\'', line, column)
                return False
            env = env.previous
        self.setError('Alterar tabla inexistente', line, column)
        return False

    def renameTo(self, id: str, newId: str, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                table = env.tables.get(id.lower())
                if table:
                    table.renameTo(newId.lower())
                    env.tables[newId.lower()] = table
                    del env.tables[id.lower()]
                    self.setPrint(f'Tabla \'{id.lower()}\' renombrada como {newId.lower()}. {line}:{column + 1}')
                    return True
            env = env.previous
        self.setError(f'La tabla \'{id.lower()}\' no existe', line, column)
        return False

    def renameColumn(self, id: str, currentColumn: str, newColumn: str, line: int, column: int) -> bool:
        env: Env = self
        while env:
            if id.lower() in env.tables:
                if currentColumn.lower() in env.tables.get(id.lower()).fields:
                    env.tables.get(id.lower()).renameColumn(currentColumn.lower(), newColumn.lower())
                    self.setPrint(f'Columna {currentColumn.lower()} actualizada exitosamente a {newColumn.lower()}. {line}:{column + 1}')
                    return True
                self.setError(f'La columna {currentColumn.lower()} no existe en Tabla \'{id.lower()}\'', line, column)
                return False
            env = env.previous
        self.setError('Alterar tabla inexistente', line, column)
        return False

    # === UTILS ===
    def setPrint(self, print_: str):
        printConsole.append([print_])

    def selectPrint(self, select: list[list[any]]):
        printConsole.extend(select)

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