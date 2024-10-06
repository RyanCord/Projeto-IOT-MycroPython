from flask import Flask, request, jsonify

app = Flask(__name__)


entradas = 0
saidas = 0
cortes = 0


@app.route('/update', methods=['POST'])
def update_data():
    global entradas, saidas, cortes
    data = request.get_json()
    
 
    entradas = data.get('entradas', entradas)
    saidas = data.get('saidas', saidas)
    cortes = data.get('cortes', cortes)
    
    return jsonify({'status': 'Dados recebidos com sucesso!'})


@app.route('/dados', methods=['GET'])
def get_data():
    return jsonify({
        'entradas': entradas,
        'saidas': saidas,
        'cortes': cortes
    })

if __name__ == '__main__':
    app.run(debug=True)