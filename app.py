from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
import jwt
import mysql.connector
from mysql.connector import Error
import datetime

app = Flask(__name__) #CREAMOS UNA INSTACIA DE NUESTRA APLICACION
app.config['SECRET_KEY'] = 'SECRET_KEY'
CORS(app)


def connectDB():
    try: 
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='usuarios',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar con la base de datos")
        return None



@app.route('/', methods=['GET'])
@cross_origin(origins='*')  
def hello():
    return jsonify({'respones': 'HOLA'})


@app.route('/login', methods=['POST'])
@cross_origin(origins='*')  
def login():
    auth = request.json

    if auth['username'] == 'username' and auth['password'] == 'password':
        token =  jwt.encode(
            {'user': auth['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token}), 200
    else: 
        return jsonify({'message': 'Invalid credentials'}), 401
   
    
def validaToken(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    


@app.route('/users', methods=['GET'])
@cross_origin(origins='*')  
def users():
    token = request.headers.get('x-acces-token')
    if not token:
        return jsonify({'message': 'No se ingreso token'})
    elif validaToken(token):
        conn = connectDB()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios')
        user = cursor.fetchall()
        cursor.close()
        return jsonify(user),200
    return jsonify({'message': 'Error interno del servicio'}), 500
   


if __name__ == '__main__':
    app.run(debug=True)