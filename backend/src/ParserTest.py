from interpreter.Parser import *
from statements.Abstracts.Expression import Expression
from statements.Abstracts.Instruction import Instruction
from statements.Env.Env import Env
from utils.Outs import getStringOuts
from utils.TypeExp import TypeExp
from utils.TypeInst import TypeInst

input = open('../../Inputs/Input1.sql', encoding='utf-8').read()
Scanner.lineno = 1
instructions: list[Instruction] = parser.parse(input)

globalEnv: Env = Env(None, 'Global')

for instruction in instructions:
    try:
        if isinstance(instruction, Instruction) and instruction.typeInst == TypeInst.INIT_FUNCTION:
            instruction.execute(globalEnv)
    except ValueError as e: pass

for instruction in instructions:
    try:
        if isinstance(instruction, Instruction) and instruction.typeInst != TypeInst.INIT_FUNCTION:
            instruction.execute(globalEnv)
        elif isinstance(instruction, Expression) and instruction.typeExp == TypeExp.CALL_FUNC:
            instruction.execute(globalEnv)
    except ValueError as e: print(e)

print(getStringOuts())