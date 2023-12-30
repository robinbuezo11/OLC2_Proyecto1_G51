from utils.TypeError import TypeError

class Error:
    def __init__(self, line: int, column: int, type: TypeError, description: str):
        self.line = line
        self.column = column
        self.type = type
        self.description = description

    def __str__(self) -> str:
        return f'→ Error {self.type.value}, {self.description}. {self.line}:{self.column}'

    def getData(self) -> list[str]:
        return [self.type.value, self.description, str(self.line), str(self.column)]
    
    def getDot(self) -> str:
        if self.type == TypeError.LEXICAL:
            return f'<tr><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td><td bgcolor="white">{self.type}</td><td bgcolor="white">{self.description}</td></tr>'
        elif self.type == TypeError.SYNTAX:
            return f'<tr><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td><td bgcolor="white">{self.type}</td><td bgcolor="white">{self.description}</td></tr>'
        elif self.type == TypeError.SEMANTIC:
            return f'<tr><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td><td bgcolor="white">{self.type}</td><td bgcolor="white">{self.description}</td></tr>'
        else:
            return f'<tr><td bgcolor="white">{self.line}</td><td bgcolor="white">{self.column}</td><td bgcolor="white">{self.type}</td><td bgcolor="white">{self.description}</td></tr>'