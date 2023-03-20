
from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS


from model.bd import configu
from flask_mysqldb import MySQL

from model.login import ModelLogin 
from model.user import UserN 
app = Flask(__name__)
CORS(app)

##Rutas
app.config['MYSQL_DB'] = 'appsalud'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
dataBase = MySQL(app)

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return '<h1>Metodo GET -Error-</h1>'
    elif request.method == 'POST':
        userDesdeCliente =  request.json

        userQllega = UserN( 0 ,userDesdeCliente['username'] , userDesdeCliente['password'] , '' , '')
        loggues__user = ModelLogin.login(dataBase,userQllega)
        if loggues__user!=None:
            if loggues__user.password:
               # obtener el token 
                tokenLogin =  get_token(loggues__user.id,loggues__user.fullname)

                return {'token' : tokenLogin,
                        'acceso' : True,
                        'fullname' : loggues__user.fullname,
                        'idUser': loggues__user.id,
                        'username' : loggues__user.username
                        }
            
            else:
                return {'token':False, 'acceso':False, 'description': 'Contraseña incorrecta'}        
        elif loggues__user == None:
            return {'token':False, 'acceso':False, 'description': 'Usuario no existe'}
       
       
# @app.route('/hola')
# def hola():
#     cursor = dataBase.connection.cursor()
#     sql = """SELECT idusuarios, usuario ,password,nombre, rol_idrol FROM usuarios 
#         WHERE usuario = '{}'""".format('fdejesusmercado')
#     cursor.execute(sql)
#     row = cursor.fetchone()
#     if row != None:
#         userRetur = UserN(row[0],row[1],UserN.check_password(row[2],'123456789'),row[4],row[3])
#         if userRetur.password:
#              return """<h1> Bienvendio al sistema '{}'</h1>""".format(userRetur.fullname)
#         else:
#             return 'contraseña incorrecta'
           
#     else:
#         return 'nada'   

# funcion para generar token
def get_token(idUser,userName):
    # Crear el payload
    payload = {'user_id': idUser, 'username': userName}
    
    # Generar el JWT
    token = jwt.encode(payload, 'secreto', algorithm='HS256')
    
    # Devolver el token como respuesta
    return token
if __name__ == '__main__':
    app.run(port = 3000,debug = True)
    app.config.from_object(configu['db'])
     


