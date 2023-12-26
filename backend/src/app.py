from flask import Flask, jsonify, request
from flask_cors import CORS
from interpreter.Parser import *
from statements.Abstracts.Expression import Expression
from statements.Abstracts.Instruction import Instruction
from statements.Env.Env import Env
from utils.Outs import getStringOuts, getPrintConsole, resetOuts
from utils.TypeExp import TypeExp
from utils.TypeInst import TypeInst
from utils.ManageXml import ManageXml

xml = ManageXml("..\\backend\\files\\data.xml")

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
    print(data['input'])
    instructions = parser.parse(data['input'])
    globalEnv = Env(None, 'Global')
    resetOuts()
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

if __name__ == '__main__':
    app.run(debug=True, port=4000)