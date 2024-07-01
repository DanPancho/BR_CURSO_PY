from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__) #CREAMOS UNA INSTACIA DE NUESTRA APLICACION
app.config['SECRET_KEY'] = 'SECRET_KEY'

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'respones': 'HOLA'})


@app.route('/login', methods=['POST'])
def login():
    auth = request.json

    if auth['username'] == 'username' and auth['password'] == 'password':
        token =  jwt.encode(
            {'user': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token}), 200
    else: 
        return jsonify({'message': 'Invalid credentials'}), 401
   
    
   # return jsonify({'token', 'Credenciales no validas'}) , 401

@app.route('/user', methods=['POST'])
def user():
    token = request.headers.get('x-acces-token')
    if not token:
        return jsonify({'message': 'No se ingreso toke'})
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'TOKEN OK'})
    except jwt.ExpiredSignatureError:
        return jsonify({'response': 'Token expirado!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'response': 'Token is invalid!'}), 401


if __name__ == '__main__':
    app.run(debug=True)