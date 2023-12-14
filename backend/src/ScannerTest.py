# from Language.Scanner import *
from interpreter.Scanner import *

input = open('../../Inputs/Pruebas.sql', encoding='utf-8').read()
scanner.input(input)
while True:
    token = scanner.token()
    if not token:
        break
    print('{:<20}{:<30}{:<5}{:<5}'.format(
        token.type,
        token.value,
        token.lineno,
        token.lexpos
    ))