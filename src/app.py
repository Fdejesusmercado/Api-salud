
from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room

from model.bd import configu
from flask_mysqldb import MySQL

from model.login import ModelLogin 
from model.user import UserN 
app = Flask(__name__)
CORS(app)
#configuracion socketio
socketio = SocketIO(app,cors_allowed_origins="*")
#config db
app.config['MYSQL_DB'] = 'appsalud'
dataBase = MySQL(app)

##Rutas
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
    
@app.route('/cargarPerfil',methods = ['GET','POST'])
def cargarPerfil():
    token = request.json['token']
    print(token)
    if request.method == 'GET':
        return{'status':'GET'}
    elif request.method == 'POST':
        try:
            # Verificar firma y decodificar token
            decoded_token = jwt.decode(token, 'secreto', algorithms=['HS256'])
          
            cursor = dataBase.connection.cursor()
            sql = """SELECT nombre, apellido, rol_idrol FROM usuarios WHERE idusuarios ={} """.format(decoded_token['user_id'])
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                userRetur = UserN(decoded_token['user_id'],'','',row[0]+" "+row[1],row[2])
                documentos = cargarDocumentos(decoded_token['user_id'])
                discapacidades = cargarDiscapacidadesPorId(decoded_token['user_id'])
               
                return jsonify({'fullname':userRetur.fullname,
                                'cargo':userRetur.cargo,
                                'documentos':documentos,
                                'discapacidades':discapacidades
                                })
            else:
                return None

            
        except jwt.InvalidTokenError:
        # Manejar errores de token inválido
            return
    else:        
        return 

@app.route('/eliminarDiscapacidad',methods = ['GET','POST','PUT']) 
def eliminarDiscapacidad():
    cursor = dataBase.connection.cursor()
    dis_eliminar = request.json['dis_eliminar']
    print(dis_eliminar)
    token = request.json['token']
    decoded_token = jwt.decode(token, 'secreto', algorithms=['HS256'])
   
    if request.method == 'GET':
        return jsonify({'status':'Tipo GET'})
    elif request.method == 'PUT':
        try:
            for i in dis_eliminar:
                print(i)
                sql = """UPDATE appsalud.discapacidades SET estado = 2  
                        WHERE tipo_discapacidad_idtipo_discapacidad = {} and usuarios_idusuarios ={} """.format(i,decoded_token['user_id'])
                print(sql)
                cursor.execute(sql)
                dataBase.connection.commit()
                
            return jsonify({'status':'Discapacidad Eliminada'})
        except:
            return jsonify({'status':'Entro al except'})

@app.route('/allDiscapacidades',methods = ['GET','POST','PUT'])
def allDiscapacidades ():
    if request.method == 'GET':
        return jsonify({'allDiscapacidades': cargarTodasLasDiscapacidades()})
    else:
        return jsonify ({'status':'Solo metodo GET'})

@app.route('/addDiscapacidad',methods = ['GET','POST','PUT'])
def addDiscapacidad():
    cursor = dataBase.connection.cursor()
    dis_add = request.json['dis_add']
    token = request.json['token']
    decoded_token = jwt.decode(token, 'secreto', algorithms=['HS256'])
   
    if request.method == 'GET':
        return jsonify({'status':'Tipo GET'})
      
    elif request.method == 'POST':
        try:
            sql = """ INSERT INTO discapacidades (usuarios_idusuarios, tipo_discapacidad_idtipo_discapacidad) VALUES (%s, %s)"""
            print(sql)
            cursor.execute(sql,(decoded_token['user_id'], dis_add))
            dataBase.connection.commit()    
            return jsonify({'status':'Discapacidad add'})
        except :
             return jsonify({'status':'Entro al except'})

@app.route('/cargarDoctoresEnMapa',methods = ['GET','POST','PUT'])
def cargarDoctoresEnMapa():
    TodosLosDoc = []
    if request.method == 'GET':
        cursor = dataBase.connection.cursor()
        sql = """SELECT idusuarios,nombre, apellido, logitud,latitud FROM appsalud.usuarios
            inner join  appsalud.ubicacion on appsalud.ubicacion.usuarios_idusuarios = appsalud.usuarios.idusuarios
            where rol_idrol = 2"""
        cursor.execute(sql)
        row = cursor.fetchall()
        if row != None:
            for i in row:
                TodosLosDoc.append({
                    'idDoctor':i[0],
                    'nombre':i[1]+" "+i[2],
                    'longi':float(i[3]),
                    'lati':float(i[4]),
                }) 
            return jsonify({'doctores':TodosLosDoc})
    else:
        return jsonify({'status':'metodo diferente de GET'})
@app.route('/cargarDoctoresPorId',methods = ['GET','POST','PUT'])
def cargarDoctoresPorId():
    if request.method == 'GET':
        try:
            cursor = dataBase.connection.cursor()
            sql = """SELECT nombre, apellido from usuarios where idusuarios = {}""".format()
            cursor.execute(sql)
            row = cursor.fetchall()
        except:
            pass
        pass

@app.route('/cargarPerfilPorId',methods = ['GET','POST','PUT'])
def cargarPerfilPorId():
    idPerfil = request.json['id']
    if request.method == 'GET':
        return{'status':'GET'}
    elif request.method == 'POST':
        try:
            # Verificar firma y decodificar token
            cursor = dataBase.connection.cursor()
            sql = """SELECT nombre, apellido, rol_idrol FROM usuarios WHERE idusuarios ={} """.format( idPerfil)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                userRetur = UserN( idPerfil,'','',row[0]+" "+row[1],row[2])
                documentos = cargarDocumentos(idPerfil)
                discapacidades = cargarDiscapacidadesPorId(idPerfil)
               
                return jsonify({'fullname':userRetur.fullname,
                                'cargo':userRetur.cargo,
                                'documentos':documentos,
                                'discapacidades':discapacidades
                                })
            else:
                return None

            
        except jwt.InvalidTokenError:
        # Manejar errores de token inválido
            return
    else:        
        return 


    pass
def cargarDocumentos(idUser):
     
     cursor = dataBase.connection.cursor()
     sql = """select appsalud.usuarios.nombre, apellido, nombreRol,url, appsalud.documentos.nombre_documento, appsalud.tipo_documento.nombre AS EXTENCION from appsalud.usuarios 
     inner join  appsalud.rol on rol.idrol = usuarios.rol_idrol
     inner join appsalud.documentos on  documentos.usuarios_idusuarios = usuarios.idusuarios
     inner join appsalud.tipo_documento on documentos.id_tipo_documento = tipo_documento.idtipo_documento
     where idusuarios = {}""".format(idUser)
     cursor.execute(sql)
     row = cursor.fetchall()
     doc = []
     if row != None:  
        for i in row:
            doc.append({
                'nombreDoc':i[4],
                'tipoDoc':i[5],
                'URL':i[3]
            })
            
        return doc
        
          
     else:
         return jsonify({'status': 'err'})
     
def cargarDiscapacidadesPorId(idUser):
     cursor = dataBase.connection.cursor()
     sql = """select idtipo_discapacidad, nombre, descripcion from appsalud.discapacidades
              inner join  appsalud.tipo_discapacidad on discapacidades.tipo_discapacidad_idtipo_discapacidad = tipo_discapacidad.idtipo_discapacidad
              where usuarios_idusuarios = {} and discapacidades.estado = 1 and tipo_discapacidad.estado = 1""".format(idUser)
     cursor.execute(sql)
     row = cursor.fetchall()
     dis = []
     if row != None:  
        for i in row:
            dis.append({
                'idDiscapacidad':i[0],
                'nombreDis':i[1],
                'descripcionDis':i[2],
            })
            
        return dis
        
          
     else:
         return jsonify({'status': 'err'})
         
def cargarTodasLasDiscapacidades():
    TodasLasDis = []  
    cursor = dataBase.connection.cursor()
    sql = """SELECT idtipo_discapacidad, nombre, descripcion FROM appsalud.tipo_discapacidad WHERE estado = 1"""
    cursor.execute(sql)
    row = cursor.fetchall()
    if row != None:
        for i in row:
            TodasLasDis.append({
                    'idDiscapacidad':i[0],
                    'nombreDis':i[1],
                    'descripcionDis':i[2],
                })
            
        return TodasLasDis  
        
    else:
         return jsonify({'status': 'err'})        



#socketio rutas
@socketio.on('addSala')
def handle_sala(id):
    token = id['id']
    decoded_token = jwt.decode(token, 'secreto', algorithms=['HS256'])
    join_room(decoded_token['user_id']) 
    print(decoded_token['user_id'])
    emit('connectTRUE',{'data':'se unio a la room {}'.format(decoded_token['user_id'])},room= decoded_token['user_id'])
    # sql = """SELECT idusuarios FROM usuarios WHERE idusuarios = {} """.format(decoded_token['user_id'])
    # cursor.execute(sql)
    # row = cursor.fetchall()
    # if row != None:
    #     for i in row:
    #        print(i[0])
    #        
    
    
    

@socketio.on('SolicitarServicio') 
def handle_solicitarServicio(id):
    token = id['token']
    decoded_token = jwt.decode(token, 'secreto', algorithms=['HS256'])
    cursor = dataBase.connection.cursor()
    sql = """SELECT nombre, apellido FROM usuarios WHERE idusuarios ={} """.format(decoded_token['user_id'])
    cursor.execute(sql)
    row = cursor.fetchall()
    if row != None:
        print(row[0][0])
        print(id['id'])
        emit('AlguienEstaEnTuSala',{'data': row[0][0] +" "+row[0][1],'idUser':decoded_token['user_id']}, room= int(id['id']))


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('response', {'data': 'Server received your message!'}, room= '1')

# funcion para generar token
def get_token(idUser,userName):
    # Crear el payload
    payload = {'user_id': idUser, 'username': userName}
    
    # Generar el JWT
    token = jwt.encode(payload, 'secreto', algorithm='HS256')
    
    # Devolver el token como respuesta
    return token
if __name__ == '__main__':
    # app.run(port = 3000,debug = True)
    socketio.run(app, port = 3000,debug = True)
    app.config.from_object(configu['db'])
     


