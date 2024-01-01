# from Language.Scanner import *
from interpreter.Scanner import *

input = open('C:\\Users\\kewin\\OneDrive\\Escritorio\\Frontend\\OLC2_PROYECTO\\OLC2_Proyecto1_G51\\Inputs\Input1.sql', encoding='utf-8').read()
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