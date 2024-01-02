from statements.Objects.Table import Field
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type
from utils.TypeExp import TypeExp
from statements.Env.AST import AST, ReturnAST
from statements.Abstracts.Expression import Expression
from statements.Env.Env import Env

class Return(Expression):
    def __init__(self, line: int, column: int, exp: Expression):
        super().__init__(line, column, TypeExp.RETURN)
        self.exp = exp

    def setField(self, _: dict[str, Field]) -> any:
        pass

    def execute(self, env: Env) -> ReturnType:
        if self.exp:
            value: ReturnType = self.exp.execute(env)
            return ReturnType(value.value, value.type)
        return ReturnType(self.typeExp, Type.NULL)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        c3dgen.addComment('--------- Return ----------')
        if self.exp:
            exp: ReturnC3D = self.exp.compile(env, c3dgen)
            if exp.type != Type.BOOLEAN:
                c3dgen.addSetStack('P', exp.strValue)
            else:
                tmp: str = c3dgen.newLbl()
                c3dgen.addLabel(exp.trueLbl)
                c3dgen.addSetStack('P', '1')
                c3dgen.addGoto(tmp)
                c3dgen.addLabel(exp.falseLbl)
                c3dgen.addSetStack('P', '0')
                c3dgen.addLabel(tmp)
            c3dgen.addGoto(env.returnLbl)
            c3dgen.addComment('------- Fin Return --------')
            return None
        c3dgen.addSetStack('P', '0')
        c3dgen.addGoto(env.returnLbl)
        c3dgen.addComment('------- Fin Return --------')
        return None

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="RETURN"];'
        if self.exp:
            value1: ReturnAST = self.exp.ast(ast)
            dot += '\n' + value1.dot
            dot += f'\nnode_{id} -> node_{value1.id};'
        return ReturnAST(dot, id)