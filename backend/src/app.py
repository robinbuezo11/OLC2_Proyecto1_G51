from flask import Flask, jsonify, request
from flask_cors import CORS
from interpreter.Parser import *
from statements.Abstracts.Expression import Expression
from statements.Abstracts.Instruction import Instruction
from statements.Env.Env import Env
from utils.Outs import getStringOuts
from utils.TypeExp import TypeExp
from utils.TypeInst import TypeInst

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Bienvenido a XSQL'})

@app.route('/api/exec', methods=['POST'])
def exec():
    data = request.get_json()
    print(data['input'])
    instructions = parser.parse(data['input'])
    globalEnv = Env(None, 'Global')
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

    result = getStringOuts()
    print(result)

    return jsonify({
        'status': 'success',
        'message': 'Ejecutado correctamente',
        'result': result,
        'error': ''
    })

if __name__ == '__main__':
    app.run(debug=True, port=4000)