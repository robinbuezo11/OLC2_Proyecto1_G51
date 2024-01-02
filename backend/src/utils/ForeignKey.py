class ForeignKey:
    def __init__(self, line: int, column: int, localAttrib: str, externalTable: str, externalAttrib: str):
        self.line = line
        self.column = column
        self.localAttrib = localAttrib
        self.externalTable = externalTable
        self.externalAttrib = externalTable