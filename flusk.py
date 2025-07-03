# Creamos objeto Flask con el name del ar
app = Flask(__namee__)


@app.route('/', methods=['GET'])
def inicio():
    mensaje = "Hola"
    return mensaje


@app.route('/api/datos', methods=['GET'])
def devolverDatos():
    response = {'datos': 'Mis datos de la BD'}
    return jsonify(response)


@app.route('/api/datos/<id>', methods=['GET'])
def devolverDato(id):
    response = {'Numero': 'Mis dato ' + id, 'apellido': 'Rey'}
    return jsonify(response)


@app.route('/api/alta', methods=['POST'])
def Alta():
    response = {'Mensaje': 'Alta'}
    return jsonify(response)


@app.route('/api/modificar/<id>', methods=['PUT'])
def Modificar(id):
    response = {'Mensaje': 'Dato modificado' + id}
    return jsonify(response)


@app.route('/api/eliminar/<id>', methods=['DELETE'])
def delete_user(id):
    response = {'Mensaje': 'Dato eliminado' + id}
    return jsonify(response)

# Ejecutamos en modo depuración
app.run(debug=True)