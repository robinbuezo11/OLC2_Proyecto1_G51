from utils.Error import Error
from utils.Token import Token

printConsole: list[str] = []
errors: list[Error] = []
tokens: list[Token] = []

def getStringOuts() -> str:
    out = ''
    out += '\n'.join(printConsole)
    if len(errors) > 0:
        if out != '':
            out += '\n\n↳ ERRORES\n'
        else:
            out += '↳ ERRORES\n'
        out += '\n'.join(str(error) for error in errors)
    return out

def getErrors():
    dot = 'digraph Errores {graph[fontname="Arial" labelloc="t" bgcolor="#252526" fontcolor="white"];node[shape=none fontname="Arial"];label="Errores";table[label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="3"><tr><td bgcolor="#009900" width="100"><font color="#FFFFFF">No.</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Linea</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Columna</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Tipo De Error</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Descripcion</font></td></tr>'
    for i in range(len(errors)):
        errors[i]
        dot += errors[i].getDot(i + 1)
    
    dot += '</table>>];}'
    return dot

def getTokens():
    dot = 'digraph Tokens {graph[fontname="Arial" labelloc="t" bgcolor="#252526" fontcolor="white"];node[shape=none fontname="Arial"];label="Tokens";table[label=<<table border="0" cellborder="1" cellspacing="0" cellpadding="3"><tr><td bgcolor="#009900" width="100"><font color="#FFFFFF">No.</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Linea</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Columna</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Lexema</font></td><td bgcolor="#009900" width="100"><font color="#FFFFFF">Token</font></td></tr>'
    for i in range(len(tokens)):
        tokens[i].num = i + 1
        dot += tokens[i]
    dot += '</table>>];}'
    return dot


def resetOuts():
    printConsole.clear()
    errors.clear()
    tokens.clear()

def getPrintConsole():
    return printConsole