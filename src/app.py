from flask import Flask, request
from model.bd import config
from flask_mysqldb import MySQL

from model.login import ModelLogin 
from model.user import UserN 
app = Flask(__name__)

##Rutas
dataBase = MySQL(app)
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        userQllega = UserN(0,'admin','123456789')
        loggues__user = ModelLogin.login(dataBase,userQllega)
        if loggues__user !=None:
            if loggues__user.password:
                return '<h1>Error...</h1>'
                
        else:
            return '<h1> User incorrecto huevo</h1>'

@app.route('/hola')
def hola():
    cursor = dataBase.connection.cursor()
    sql = """SELECT idusuarios, usuario ,password,nombre FROM usuarios 
        WHERE usuario = '{}'""".format('admin')
    cursor.execute(sql)
    row = cursor.fetchone()
    if row != None:
        userRetur = UserN(row[0],row[1],UserN.check_password(row[2],'123456789'),row[3])
        return userRetur
    


if __name__ == '__main__':
    app.run(port = 3000,debug = True)
    app.config.from_object(config['db'])
