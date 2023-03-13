from .user import UserN

@classmethod
class ModelLogin ():
  
    def login(self,db,userQllega):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idusuarios, usuario ,password,nombre FROM usuarios 
            WHERE usuario = '{}'""".format(userQllega.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                userRetur = UserN(row[0],row[1],UserN.check_password(row[2],userQllega.password),row[3])
                return userRetur
            else:
                return None
        except Exception as ex:
            raise Exception (ex)
        
    