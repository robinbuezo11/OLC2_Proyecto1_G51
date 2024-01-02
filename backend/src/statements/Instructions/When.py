from statements.Abstracts.Instruction import Instruction
from statements.Abstracts.Expression import Expression
from utils.TypeInst import TypeInst
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class When(Instruction):
    def __init__(self, line: int, column: int, when_: Expression, result: Expression):
        super().__init__(line, column, TypeInst.WHEN)
        self.when_ = when_
        self.result = result
        self.whenEvaluate = None

    def setWhen(self, whenEvaluate: ReturnType):
        self.whenEvaluate = whenEvaluate

    def execute(self, env: Env) -> ReturnType:
        envWhen: Env = Env(env, f'{env.name} when')
        when_: ReturnType = self.when_.execute(envWhen)
        if self.whenEvaluate:
            whenE: ReturnType = self.whenEvaluate
            envWhen.name = f'{envWhen.name} {when_.value}'
            if when_.value == whenE.value:
                result: ReturnType = self.result.execute(envWhen)
                return result
        else:
            condition: ReturnType = self.when_.execute(env)
            if condition.value:
                return self.result.execute(env)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="WHEN"];'
        dot += f'node_{id}_cond[label="CONDICION"];'
        dot += f'node_{id}_result[label="RESULT"];'
        cond: ReturnAST = self.when_.ast(ast)
        result: ReturnAST = self.result.ast(ast)
        dot += '\n' + cond.dot
        dot += '\n' + result.dot
        dot += f'\nnode_{id}_cond -> node_{cond.id};'
        dot += f'\nnode_{id}_result -> node_{result.id};'
        dot += f'\nnode_{id} -> node_{id}_cond;'
        dot += f'\nnode_{id} -> node_{id}_result;'
        return ReturnAST(dot, id)