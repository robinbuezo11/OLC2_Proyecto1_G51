from flask import Flask, jsonify, request
from flask_cors import CORS
from interpreter.Parser import *
from statements.Abstracts.Expression import Expression
from statements.Abstracts.Instruction import Instruction
from statements.Env.Env import Env
from statements.Env.AST import AST
from utils.Outs import getStringOuts, getPrintConsole, resetOuts
from utils.TypeExp import TypeExp
from utils.TypeInst import TypeInst
from utils.Global import *
from statements.Env.SymbolTable import SymbolTable
from utils.Outs import getErrors
from utils.Outs import getTokens


dotAst = ''


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Bienvenido a XSQL'})

@app.route('/api/getStruct', methods=['GET'])
def getStruct():
    try:
        res = xml.getStruct()
        if res:
            return jsonify({
                'success': True,
                'message': 'Estructura obtenida correctamente',
                'result': res,
                'error': ''
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al obtener la estructura',
                'result': '',
                'error': 'No existen bases de datos'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al procesar la petición',
            'result': '',
            'error': str(e)
        })
    

@app.route('/api/exec', methods=['POST'])
def exec():
    data = request.get_json()
    Scanner.lineno = 1
    instructions = parser.parse(data['input'])
    globalEnv = Env(None, 'Global')
    resetOuts()

    global dotAst
    dotAst = 'digraph G{\nnode[color="white" fontcolor="white"];\nedge[dir=none color="white"];\nbgcolor = "#0D1117";'
    dotAst += '\nnode_r[label="INSTRUCTIONS"];'
    ast = AST()    
    for instruction in instructions:
        try:
            if isinstance(instruction, Instruction) and instruction.typeInst == TypeInst.INIT_FUNCTION:
                instruction.execute(globalEnv)
                resultAST = instruction.ast(ast)
                dotAst += '\n' + resultAST.dot
                dotAst += f'\nnode_r -> node_{resultAST.id};'
        except ValueError as e: pass

    for instruction in instructions:
        try:
            if isinstance(instruction, Instruction) and instruction.typeInst != TypeInst.INIT_FUNCTION:
                instruction.execute(globalEnv)
                resultAST = instruction.ast(ast)
                dotAst += '\n' + resultAST.dot
                dotAst += f'\nnode_r -> node_{resultAST.id}'
            elif isinstance(instruction, Expression) and instruction.typeExp == TypeExp.CALL_FUNC:
                instruction.execute(globalEnv)
                resultAST = instruction.ast(ast)
                dotAst += '\n' + resultAST.dot
                dotAst += f'\nnode_r -> node_{resultAST.id}'
        except ValueError as e: print(e)
    dotAst += '\n}'

    result = getPrintConsole()

    # result.insert(0, 'Resultado')
    # data = []
    # for res in result:
    #     data.append([res])


    return jsonify({
        'success': True,
        'message': 'Ejecutado correctamente',
        'result': result,
        'error': ''
    })

@app.route('/api/createDB', methods=['POST'])
def createDB():
    try:
        data = request.get_json()
        print(data['dbName'])
        create = True if data['action'] == 'create' else False
        res = xml.createDataBase(data['dbName']) if create else xml.dropDatabase(data['dbName'])
        if res:
            return jsonify({
                'success': True,
                'message': 'Base de datos creada correctamente' if create else 'Base de datos eliminada correctamente',
                'result': '',
                'error': ''
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al crear la base de datos' if create else 'Error al eliminar la base de datos',
                'result': '',
                'error': 'Base de datos ya existente' if create else 'Base de datos no existente'
            })  
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al obtener los parametros',
            'result': '',
            'error': str(e)
        })
    
@app.route('/api/getAst', methods=['GET'])
def getAst():
    return jsonify({
        'success': True,
        'message': 'AST generado correctamente',
        'result': dotAst,
        'error': ''
    })

@app.route('/api/getSymbols', methods=['GET'])
def getSymbols():
    try:
        res = SymbolTable.symTable.getDot()
        print(res)
        if res:
            return jsonify({
                'success': True,
                'message': 'Tabla de simbolos obtenida correctamente',
                'result': res,
                'error': ''
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al obtener la tabla de simbolos',
                'result': '',
                'error': 'No existen bases de datos'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al procesar la petición',
            'result': '',
            'error': str(e)
        })
    
@app.route('/api/getError', methods=['GET'])
def getError():
    try:
        res = getErrors()
        print(res)
        if res:
            return jsonify({
                'success': True,
                'message': 'Errores obtenidos correctamente',
                'result': res,
                'error': ''
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al obtener los errores',
                'result': '',
                'error': 'No existen errores'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al procesar la petición',
            'result': '',
            'error': str(e)
        })

@app.route('/api/getTokens', methods=['GET'])
def getToken():
    try:
        res = getTokens()
        print(res)
        if res:
            return jsonify({
                'success': True,
                'message': 'Tokens obtenidos correctamente',
                'result': res,
                'error': ''
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al obtener los tokens',
                'result': '',
                'error': 'No existen tokens'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al procesar la petición',
            'result': '',
            'error': str(e)
        })


if __name__ == '__main__':
    app.run(debug=True, port=4000)