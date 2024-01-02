import math
from statements.Abstracts.Expression import Expression
from statements.Env.Env import Env
from utils.Type import Type, ReturnType
from utils.Attribute import Attribute
from utils.ForeignKey import ForeignKey
#-------- DESCOMENTANDO AQUI ---------
from statements.Expressions.Field import Field as F

class Data:
    def __init__(self, type: Type, value: any):
        self.type = type
        self.value = value

    def update(self, value: any):
        self.value = value

    def getData(self) -> ReturnType:
        return ReturnType(self.value, self.type)

class Field:
    def __init__(self, type: Type, values: list[Data], length: int = None, notNull: bool = False, isPrimary: bool = False):
        self.type = type
        self.values = values
        self.length = length
        self.notNull = notNull
        self.isPrimary = isPrimary

    def slice(self):
        self.values.clear()

    def updateLength(self, n: int):
        if n > self.length:
            self.length = n

class Table:
    def __init__(self, name: str, attribs: list[Attribute | ForeignKey]):
        self.fields: dict[str, Field] = {}
        self.rows: int = 0
        for attrib in attribs:
            if type(attrib) == Attribute:
                self.fields[attrib.id.lower()] = Field(attrib.type, [], len(attrib.id), attrib.props['notNull'], attrib.props['primaryKey'])
            elif type(attrib) == ForeignKey:
                pass
        self.name = name

    def insert(self, env: Env, fields: dict[str, list[any]], line: int, column: int) -> bool:
        if fields and self.validate(env, fields, line, column):
            for name, field in fields.items():
                self.fields.get(name).values.append(Data(field[0], field[1]))
                self.fields.get(name).updateLength(len(str(field[1])))
            self.rows += 1
            return True
        return False

    def validate(self, env: Env, fields: dict[str, list[any]], line: int, column: int) -> bool:
        for name, field in fields.items():
            if self.fields.get(name).type == field[0] or \
            self.fields.get(name).type == Type.DECIMAL and field[0] == Type.INT or \
            self.fields.get(name).type == Type.NCHAR and field[0] == Type.NVARCHAR:
                continue
            env.setError(f'No coincide el tipo de dato para la columna {name} en la tabla {self.name}', line, column)
            return False
        return True

    def validateFields(self, names: list[str]) -> bool:
        for name in names:
            if not name.lower() in self.fields:
                return False
        return True

    def truncate(self):
        for name, field in self.fields.items():
            field.slice()
            self.fields[name] = field
        self.rows = 0

    def addColumn(self, newColumn: str, type: Type):
        self.fields[newColumn.lower()] = Field(type, [], len(newColumn))
        for i in range(self.rows):
            self.fields.get(newColumn.lower()).values.append(Data(Type.NULL, 'NULL'))
            self.fields.get(newColumn.lower()).updateLength(len(newColumn))

    def dropColumn(self, column: str):
        del self.fields[column.lower()]

    def renameTo(self, newId: str):
        self.name = newId.lower()

    def renameColumn(self, currentColumn: str, newColumn: str):
        field = self.fields.get(currentColumn.lower())
        if field:
            self.fields[newColumn] = field
            self.fields.get(newColumn).updateLength(len(newColumn))
            del self.fields[currentColumn.lower()]

    def createTmpFields(self) -> dict[str, Field]:
        newFields: dict[str, Field] = {}
        for name, field in self.fields.items():
            newFields[name] = Field(field.type, [], len(name), field.notNull, field.isPrimary)
        return newFields

    def deleteWhere(self, condition: Expression, env: Env):
        tmpFields: dict[str, Field]
        resultFields: dict[str, Field] = self.createTmpFields()
        result: ReturnType
        newRows: int = 0
        for i in range(self.rows):
            tmpFields = self.createTmpFields()
            for name, field in self.fields.items():
                tmpFields.get(name).values.append(Data(field.values[i].type, field.values[i].value))
            condition.setField(tmpFields)
            result = condition.execute(env)
            if result.type == Type.BOOLEAN and str(result.value) == 'False':
                for name, field in tmpFields.items():
                    resultFields.get(name).values.append(Data(field.values[0].type, field.values[0].value))
                    resultFields.get(name).updateLength(len(str(field.values[0].value)))
                newRows += 1
        self.fields = resultFields
        if newRows != self.rows:
            self.rows = newRows

    def updateWhere(self, condition: Expression, fields: list[str], values: list[Expression], env: Env):
        tmpFields: dict[str, Field]
        result: ReturnType
        newValue: ReturnType
        for i in range(self.rows):
            tmpFields = self.createTmpFields()
            for name, field in self.fields.items():
                tmpFields.get(name).values.append(Data(field.values[i].type, field.values[i].value))
            condition.setField(tmpFields)
            result = condition.execute(env)
            if result.type == Type.BOOLEAN and str(result.value) == 'True':
                for j in range(len(fields)):
                    if fields[j].lower() in self.fields:
                        values[j].setField(tmpFields)
                        newValue = values[j].execute(env)
                        if newValue.type == self.fields.get(fields[j].lower()).type:
                            self.fields.get(fields[j].lower()).values[i].update(newValue.value)
                            self.fields.get(fields[j].lower()).updateLength(len(str(newValue.value)))
                            continue
                        env.setError(f'No coincide el tipo de dato para la columna {fields[j].lower()} en la Tabla {self.name}', values[j].line, values[j].column)
                        return
                    env.setError(f'No existe el campo {fields[j].lower()} en Tabla {self.name}', values[j].line, values[j].column)
                    return

    def getAllFieldsTitle(self) -> list[list[any]]:
        fieldsTitle: list[list[any]] = []
        for field in self.fields:
            fieldsTitle.append([F(0, 0, field), field])
        return fieldsTitle

    def getTitles(self, fieldsTitle: list[list[any]] or str) -> list[list[str]]:
        newFieldsTitle: list[list[str]] = []
        newTitle: any
        for title in fieldsTitle:
            title[0].setIsFieldName(True)
            newTitle = title[0].execute(None).value.lower()
            newFieldsTitle.append([newTitle, newTitle if title[1] == '' else title[1].lower()])
        return newFieldsTitle

    def createSelectFields(self, titles: list[list[str]]) -> dict[str, Field]:
        newFields: dict[str, Field] = {}
        type: Type
        for field in titles:
            type = self.fields.get(field[0]).type
            newFields[field[1]] = Field(type if type else Type.NULL, [], len(field[1]), False, False)
        return newFields

    def select(self, fields: list[list[any]] or str, condition: Expression, env: Env) -> str:
        titles: list[list[str]] = []
        if type(fields) == str and fields == '*':
            fields = self.getAllFieldsTitle()
        titles = self.getTitles(fields)
        selectedFields: dict[str, Field] = self.createSelectFields(titles)
        tmpFields: dict[str, Field]
        result: ReturnType
        resField: Data
        newRows: int = 0
        for i in range(self.rows):
            tmpFields = self.createTmpFields()
            for name, field in self.fields.items():
                tmpFields.get(name).values.append(Data(field.values[i].type, field.values[i].value))
            condition.setField(tmpFields)
            result = condition.execute(env)
            if result.type == Type.BOOLEAN and str(result.value) == 'True':
                for field in titles:
                    resField = self.fields.get(field[0]).values[i]
                    selectedFields.get(field[1]).values.append(Data(resField.type if resField.type else Type.NULL, resField.value))
                    selectedFields.get(field[1]).updateLength(len(str(resField.value)))
                newRows += 1
        return self.getTableList(selectedFields, newRows)

    def getTable(self, fields: dict[str, Field], rows: int) -> str:
        consult: str = ''
        start: str = ''
        header: str = ''
        middle: str = ''
        end: str = ''
        lengths: list[int] = []
        data: list[list[any]] = []
        for name, field in fields.items():
            if header != '':
                start += '═╦═'
                middle += '═╬═'
                header += ' ║ '
                end += '═╩═'
            start += '═' * field.length
            middle += '═' * field.length
            header += f'{name}' + ' ' * (field.length - len(name))
            end += '═' * field.length
            lengths.append(field.length)
            data.append(field.values)
        title = f'{self.name}'
        mitad = math.trunc(len(header) / 2)
        mitadTitle = math.trunc(len(title) / 2)
        consult += f'    ╔═{"═" * (len(header))}═╗\n'
        consult += f'    ║ {" " * (mitad - mitadTitle) + title.ljust(len(header) - mitad + mitadTitle)} ║\n'
        consult += f'    ╠═{start}═╣\n'
        consult += f'    ║ {header} ║\n'
        consult += f'    ╠═{middle}═╣\n'
        row: str = ''
        for j in range(rows):
            row = ''
            for i in range(len(data)):
                if row != '':
                    row += ' ║ '
                row += str(data[i][j].value).ljust(lengths[i])
            consult += f'    ║ {row} ║\n'
        consult += f'    ╚═{end}═╝\n'
        return consult

    def getFieldsRow(self) -> dict[str, list[any]]:
        base: dict[str, list[any]] = {}
        for name, field in self.fields.items():
            base[name] = [field.type, 'NULL']
        return base
    
#---------------------------------- SELECT RETURN IN FORMAT REQUIRED TO FRONTEND ----------------------------------
    
    def getTableList(self, fields: dict[str, Field], rows: int) -> str:
        data: list[list[any]] = []
        header: list[str] = []
        for name, _ in fields.items():
            header.append(name)
        data.append(header)
        
        for i in range(rows):
            row: list[any] = []
            for name, field in fields.items():
                row.append(field.values[i].value)
            data.append(row)
        return data