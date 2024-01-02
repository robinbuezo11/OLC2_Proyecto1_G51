from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.TypeInst import TypeInst
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class Select_prt(Instruction):
    def __init__(self, line: int, column: int, expression: list[list[any]]):
        super().__init__(line, column, TypeInst.SELECT)
        self.expression = expression

    def execute(self, env: Env) -> any:
        value: ReturnType
        for i in range(len(self.expression)):
            value = self.expression[i][0].execute(env) if self.expression[i] else None
            if value:
                if self.expression[i][1] != '':
                    env.setPrint(self.expression[i][1] + ': ' + str(value.value))
                else:
                    env.setPrint(value.value)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        c3dgen.addComment('---------- Print ----------')
        if len(self.expression) > 0:
            for exp in self.expression:
                value: ReturnC3D = exp[0].compile(env, c3dgen)
                if value.type in [Type.INT, Type.BIT]:
                    c3dgen.addPrintf('d', '(int) ' + value.strValue)
                elif value.type == Type.DECIMAL:
                    c3dgen.addPrintf('f', '(float) ' + value.strValue)
                elif value.type == Type.NULL:
                    c3dgen.addPrint('NULL')
                else:
                    tmp1: str = c3dgen.newTmp()
                    tmp2: str = c3dgen.newTmp()
                    c3dgen.addExpression(tmp1, 'P', '+', str(env.size))
                    c3dgen.addExpression(tmp1, tmp1, '+', '1')
                    c3dgen.addSetStack(tmp1, value.strValue)
                    c3dgen.newEnv(env.size)
                    c3dgen.generatePrintString()
                    c3dgen.addCall('_printString')
                    c3dgen.addGetStack(tmp2, 'P')
                    c3dgen.prevEnv(env.size)
            c3dgen.addPrint("\n")
        c3dgen.addComment("-------- Fin Print --------")

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="SELECT"];'
        value: ReturnAST
        for i in range(len(self.expression)):
            value = self.expression[i][0].ast(ast)
            if self.expression[i][1] != '':
                dot += f'\nnode_{id}_AS{i}[label="AS"];'
                dot += f'\nnode_{id} -> node_{id}_AS{i};'
                dot += f'\n{value.dot}'
                dot += f'\nnode_{id}_AS{i} -> node_{value.id};'
                dot += f'\nnode_{id}_ASTXT{i}[label="{self.expression[i][1]}"];'
                dot += f'\nnode_{id}_AS{i} -> node_{id}_ASTXT{i};'
            else:
                dot += f'\n{value.dot}'
                dot += f'\nnode_{id} -> node_{value.id};'
        return ReturnAST(dot, id)