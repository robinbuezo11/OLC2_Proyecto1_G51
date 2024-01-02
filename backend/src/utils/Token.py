class Token:
    def __init__(self, line: int, column: int, lexeme: str, token: str):
        self.num = 0
        self.line = line
        self.column = column + 1
        self.lexeme = lexeme
        self.token = token

    def getDot(self) -> str:
        if self.token != None:
            return f'<tr><td>{self.num}</td><td>{self.line}</td><td>{self.column}</td><td>{self.lexeme}</td><td>{self.token}</td></tr>'
        elif self.lexeme != None:
            return f'<tr><td>{self.num}</td><td>{self.line}</td><td>{self.column}</td><td>{self.lexeme}</td><td>Desconocido</td></tr>'
        else:
            return ''