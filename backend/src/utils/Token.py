class Token:
    def __init__(self, line: int, column: int, lexeme: str, token: str):
        self.line = line
        self.column = column + 1
        self.lexeme = lexeme
        self.token = token

    def getDot(self) -> str:
        return f'node{self.line}{self.column}{self.le} [label="{self.token}"];\n'