from utils.Error import Error
from utils.Token import Token

printConsole: list[str] = []
errors: list[Error] = []
tokens: list[Token] = []

def getStringOuts() -> str:
    out = ''
    global printConsole
    global errors
    out += '\n'.join(printConsole)
    if len(errors) > 0:
        if out != '':
            out += '\n\n↳ ERRORES\n'
        else:
            out += '↳ ERRORES\n'
        out += '\n'.join(str(error) for error in errors)
    return out

def getErrors():
    global errors
    return errors

def getTokens():
    global tokens
    return tokens

def resetOuts():
    global printConsole
    global errors
    global tokens
    printConsole.clear()
    errors.clear()
    tokens.clear()