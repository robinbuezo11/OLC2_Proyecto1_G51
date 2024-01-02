from statements.Abstracts.Expression import Expression
from statements.Abstracts.Instruction import Instruction
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from utils.TypeInst import TypeInst
from statements.Instructions.When import When
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class Case(Instruction):
    def __init__(self, line: int, column: int, arg: Expression, whens: list[When], else_: Expression, alias: str):
        super().__init__(line, column, TypeInst.CASE)
        self.arg = arg
        self.whens = whens
        self.else_ = else_
        self.alias = alias

    def execute(self, env: Env) -> any:
        envCase: Env = Env(env, 'case')
        if self.whens:
            if self.arg:
                arg: ReturnType = self.arg.execute(env)
                for when_ in self.whens:
                    when_.setWhen(arg)
                    when_exe: ReturnType = when_.execute(envCase)
                    if when_exe:
                        env.setPrint(f'{self.alias + ": " if self.alias else ""}' + when_exe.value + f'. {when_.line}:{when_.column}')
                        return
            else:
                for when_ in self.whens:
                    when_exe: ReturnType = when_.execute(envCase)
                    if when_exe:
                        env.setPrint(f'{self.alias + ": " if self.alias else ""}' + when_exe.value + f'. {when_.line}:{when_.column}')
                        return
        if self.else_:
            default_: ReturnType = self.else_.execute(envCase)
            if default_:
                env.setPrint(f'{self.alias + ": " if self.alias else ""}' + default_.value + f'. {self.else_.line}:{self.else_.column}')
                return

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        pass

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="CASE"];'
        arg_: ReturnAST
        when: ReturnAST
        default_: ReturnAST
        if self.arg:
            arg_ = self.arg.ast(ast)
            dot += '\n' + arg_.dot
            dot += f'\nnode_{id} -> node_{arg_.id};'
        for i in range(len(self.whens)):
            when = self.whens[i].ast(ast)
            dot += '\n' + when.dot
            dot += f'\nnode_{id} -> node_{when.id};'
        if self.else_:
            dot += f'node_{id}_else[label="ELSE"];'
            default_ = self.else_.ast(ast)
            dot += '\n' + default_.dot
            dot += f'\nnode_{id}_else -> node_{default_.id};'
            dot += f'\nnode_{id} -> node_{id}_else;'
        if self.alias:
            dot += f'\nnode_{id}_as[label="AS"];'
            dot += f'\nnode_{id}_alias[label="{self.alias}"];'
            dot += f'\nnode_{id}_as -> node_{id}_alias;'
            dot += f'\nnode_{id} -> node_{id}_as;'
        return ReturnAST(dot, id)