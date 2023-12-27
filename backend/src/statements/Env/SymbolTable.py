from SymTab import SymTab

class SymbolTable:
    def __init__(self):
        self.symbols = []

    def push(self, sym: SymTab):
        if self.validateSymbol(sym):
            self.symbols.append(sym)

    def pop(self, id):
        for i in range(len(self.symbols)):
            if self.symbols[i].id == id:
                self.symbols.pop(i)
                break

    def validateSymbol(self, sym: SymTab):
        for i in self.symbols:
            if i.hash() == sym.hash():
                return False
        return True

    def getDot(self):
        dot = 'digraph SymbolsTable {graph[fontname="Arial" labelloc="t" bgcolor="#252526" fontcolor="white"];node[shape=none fontname="Arial"];label="Tabla de Símbolos";table[label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="3"><tr><td bgcolor="#009900" width="100"><font color="#FFFFFF">No.</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Identificador</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Tipo</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Tipo de Dato</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Entorno</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Línea</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Columna</font></td></tr>'
        for i in range(len(self.symbols)):
            self.symbols[i].num = i + 1
            dot += self.symbols[i].getDot()
        dot += '</table>>];}'
        return dot

    def print(self):
        print('TABLA DE SÍMBOLOS')
        for sym in self.symbols:
            print(sym.toString())

    def splice(self):
        self.symbols.clear()

    def toString(self):
        table = '╔═' + '═'.repeat(69) + '═╗'
        table += '\n║ ' + ' '.repeat(26) + 'TABLA DE SÍMBOLOS' + ' '.repeat(26) + ' ║'
        table += '\n╠═' + '═'.repeat(20) + '═╦═' + '═'.repeat(10) + '═╦═' + '═'.repeat(15) + '═╦═' + '═'.repeat(5) + '═╦═' + '═'.repeat(7) + '═╣'
        table += '\n║ ' + 'ID'.padEnd(20) + ' ║ ' + 'TIPO'.padEnd(10) + ' ║ ' + 'ENTORNO'.padEnd(15) + ' ║ ' + 'LINEA'.padEnd(5) + ' ║ ' + 'COLUMNA'.padEnd(7) + ' ║'
        table += '\n╠═' + '═'.repeat(20) + '═╬═' + '═'.repeat(10) + '═╬═' + '═'.repeat(15) + '═╬═' + '═'.repeat(5) + '═╬═' + '═'.repeat(7) + '═╣'
        for sym in self.symbols:
            table += '\n' + sym.toString()
        table += '\n╚═' + '═'.repeat(20) + '═╩═' + '═'.repeat(10) + '═╩═' + '═'.repeat(15) + '═╩═' + '═'.repeat(5) + '═╩═' + '═'.repeat(7) + '═╝'
        return table

symTable = SymbolTable()