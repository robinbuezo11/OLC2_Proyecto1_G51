from statements.Abstracts.Expression import Expression
from statements.Env.AST import AST, ReturnAST
from statements.Env.Env import Env
from statements.Env.Symbol import Symbol
from utils.Parameter import Parameter
from statements.Instructions.Function import Function
from statements.Objects.Table import Field
from utils.TypeExp import TypeExp
from statements.C3D.C3DGen import C3DGen
from utils.Type import ReturnType, ReturnC3D, Type

class CallFunction(Expression):
    def __init__(self, line: int, column: int, id: str, args: list[Expression]):
        super().__init__(line, column, TypeExp.CALL_FUNC)
        self.id = id
        self.args = args

    def setField(self, _: dict[str, Field]) -> any:
        pass

    def execute(self, env: Env) -> ReturnType:
        func: Function = env.getFunction(self.id)
        if func:
            envFunc: Env = Env(env, f'Funcion ${self.id.lower()}')
            if len(func.parameters) == len(self.args):
                value: ReturnType
                param: Parameter
                for i in range(len(func.parameters)):
                    value = self.args[i].execute(env)
                    param = func.parameters[i] 
                    if value.type == param.type or param.type == Type.DECIMAL and value.type == Type.INT:
                        if not param.id.lower() in envFunc.ids:
                            envFunc.ids[param.id.lower()] = Symbol(value.value, param.id.lower(), param.type)
                            #symTable.push(new SymTab(param.line, param.column + 1, true, true, param.id.toLowerCase(), envFunc.name, param.type))
                            continue
                        env.setError('No puede haber parámetros distintos con el mismo nombre', param.line, param.column)
                        return
                    env.setError(f'Se esperaba un tipo de dato "{self.getType(param.type)}" para el parámetro "{param.id}"', param.line, param.column)
                    return
                execute: ReturnType = func.block.execute(envFunc)
                if execute:
                    if execute.value == TypeExp.RETURN:
                        return
                    return execute
                return
            env.setError(f'Cantidad errónea de parámetros enviados', self.line, self.column)
            return
        env.setError(f'La Función "{self.id}" no existe, línea {self.line} columna {self.column}', self.line, self.column)

    def compile(self, env: Env, c3dgen: C3DGen) -> ReturnC3D:
        func: Function = env.getFunction(self.id)
        if func:
            if len(func.parameters) == len(self.args):
                c3dgen.addComment('----- Llamada Funcion -----')
                tmp: str = c3dgen.newTmp()
                if len(func.parameters) > 0:
                    c3dgen.addComment('------- Parametros --------')
                    c3dgen.addExpression(tmp, 'P', '+', str(env.size + 1))
                    for i in range(len(func.parameters)):
                        value: ReturnC3D = self.args[i].compile(env, c3dgen)
                        param: Parameter = func.parameters[i]
                        if value.type == param.type or param.type == Type.DECIMAL and value.type == Type.INT:
                            if value.type != Type.BOOLEAN:
                                c3dgen.addSetStack(tmp, value.strValue)
                            else:
                                c3dgen.addLabel(value.trueLbl)
                                c3dgen.addSetStack(tmp, '1')
                                lbl: str = c3dgen.newLbl()
                                c3dgen.addGoto(lbl)
                                c3dgen.addLabel(value.falseLbl)
                                c3dgen.addSetStack(tmp, '0')
                                c3dgen.addLabel(lbl)
                            if i < len(func.parameters) - 1:
                                c3dgen.addExpression(tmp, tmp, '+', '1')
                            continue
                        c3dgen.addComment('----- Fin Parametros ------')
                        c3dgen.addComment('--- Fin Llamada Funcion ---')
                        return None
                    c3dgen.addComment('----- Fin Parametros ------')
                c3dgen.newEnv(env.size)
                c3dgen.addCall(self.id)
                c3dgen.addGetStack(tmp, 'P')
                c3dgen.prevEnv(env.size)
                if func.type != Type.NULL:
                    c3dgen.addComment('--- Fin Llamada Funcion ---')
                    return ReturnC3D(isTmp = True, strValue = tmp, type = func.type)
                c3dgen.addComment('--- Fin Llamada Funcion ---')
                return None
            c3dgen.addComment('--- Fin Llamada Funcion ---')
            return None
        return None

    def getType(type: Type) -> str:
        match type:
            case Type.INT:
                return "INT"
            case Type.DECIMAL:
                return "DECIMAL"
            case Type.NVARCHAR:
                return "NVARCHAR"
            case Type.BOOLEAN:
                return "BOOLEAN"
            case Type.DATE:
                return "DATE"
            case Type.TABLE:
                return "TABLE"
            case _:
                return "NULL"

    def ast(self, ast: AST) -> ReturnAST:
        id = ast.getNewID()
        dot = f'node_{id}[label="CALL FUNC"]'
        dot += f'\nnode_{id}_name[label="{self.id}"]'
        dot += f'\nnode_{id} -> node_{id}_name'
        param: ReturnAST
        if len(self.args) > 0:
            for i in range(len(self.args)):
                param = self.args[i].ast(ast)
                dot += '\n' + param.dot
                dot += f'\nnode_{id}_name -> node_{param.id}'
        return ReturnAST(dot, id)