from interpreter.Parser import *
from statements.Abstracts.Expression import Expression
from statements.Abstracts.Instruction import Instruction
from statements.Env.Env import Env
from statements.Env.AST import AST
from utils.Outs import getStringOuts
from utils.TypeExp import TypeExp
from utils.TypeInst import TypeInst

input = open('../../Inputs/Pruebas.sql', encoding='utf-8').read()
Scanner.lineno = 1
instructions: list[Instruction] = parser.parse(input)

ast: AST = AST()
globalEnv: Env = Env(None, 'Global')
dot = 'digraph G{\nnode[color="white" fontcolor="white"];\nedge[dir=none color="white"];\nbgcolor = "#0D1117";'
dot += '\nnode_r[label="INSTRUCTIONS"];'
for instruction in instructions:
    try:
        if isinstance(instruction, Instruction) and instruction.typeInst == TypeInst.INIT_FUNCTION:
            instruction.execute(globalEnv)
            resultAST = instruction.ast(ast)
            dot += '\n' + resultAST.dot
            dot += f'\nnode_r -> node_{resultAST.id};'
    except ValueError as e: pass

for instruction in instructions:
    try:
        if isinstance(instruction, Instruction) and instruction.typeInst != TypeInst.INIT_FUNCTION:
            instruction.execute(globalEnv)
            resultAST = instruction.ast(ast)
            dot += '\n' + resultAST.dot
            dot += f'\nnode_r -> node_{resultAST.id}'
        elif isinstance(instruction, Expression) and instruction.typeExp == TypeExp.CALL_FUNC:
            instruction.execute(globalEnv)
            resultAST = instruction.ast(ast)
            dot += '\n' + resultAST.dot
            dot += f'\nnode_r -> node_{resultAST.id}'
    except ValueError as e: print(e)
dot += '\n}'

print(getStringOuts())
print('=====================================')
print(dot)