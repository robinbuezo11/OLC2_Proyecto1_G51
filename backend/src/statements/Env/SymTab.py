from utils.Type import Type


class SymTab:
    def __init__(self, line, column, isVariable, isPrimitive, id, nameEnv, type: Type):
        self.num = 0
        self.line = line
        self.column = column
        self.isVariable = isVariable
        self.isPrimitive = isPrimitive
        self.id = id
        self.nameEnv = nameEnv
        self.type = type

    def toString(self):
        return '║ ' + f'{self.id}'.ljust(20) + ' ║ ' + f'{self.getType(self.type)}'.ljust(10) + ' ║ ' + f'{self.nameEnv}'.ljust(15) + ' ║ ' + f'{self.line}'.ljust(5) + ' ║ ' + f'{self.column}'.ljust(7) + ' ║ '

    def hash(self):
        return f'{self.id}_{self.type}_{self.nameEnv}_{self.line}_{self.column}_{self.isVariable}_{self.isPrimitive}'

    def getDot(self):
        if self.isPrimitive or self.isVariable:
            if self.isPrimitive:
                if self.isVariable:
                    return f'<tr><td bgcolor="white">{self.num}</td><td bgcolor="white">{self.id}</td><td bgcolor="white">Variable</td><td bgcolor="white">{self.getType(self.type)}</td><td bgcolor="white">{self.nameEnv}</td><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td></tr>'
                return f'<tr><td bgcolor="white">{self.num}</td><td bgcolor="white">{self.id}</td><td bgcolor="white">Función</td><td bgcolor="white">{self.getType(self.type)}</td><td bgcolor="white">{self.nameEnv}</td><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td></tr>'
        if self.type != Type.NULL:
            return f'<tr><td bgcolor="white">{self.num}</td><td bgcolor="white">{self.id}/td><td bgcolor="white">Función</td><td bgcolor="white">{self.getType(self.type)}</td><td bgcolor="white">{self.nameEnv}</td><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td></tr>'
        return f'<tr><td bgcolor="white">{self.num}</td><td bgcolor="white">{self.id}</td><td bgcolor="white">Método</td><td bgcolor="white">{self.getType(self.type)}</td><td bgcolor="white">{self.nameEnv}</td><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td></tr>'

    def getType(self, type: Type):
        switcher = {
            Type.BIT: "BIT",
            Type.INT: "INT",
            Type.DECIMAL: "DECIMAL",
            Type.NCHAR: "VARCHAR",
            Type.NVARCHAR: "VARCHAR",
            Type.DATETIME: "DATETIME",
            Type.BOOLEAN: "BOOLEAN",
            Type.DATE: "DATE",
            Type.TABLE: "TABLE",
            Type.NULL: "NULL"
        }
        return switcher.get(type, "UNKNOWN")