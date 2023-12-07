from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Bienvenido a XSQL'})

if __name__ == '__main__':
    app.run(debug=True, port=4000)