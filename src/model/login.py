from .user import UserN


class ModelLogin ():
    @classmethod
    def login(self,db,userQllega):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idusuarios, usuario ,password,nombre,rol_idrol FROM usuarios 
            WHERE usuario = '{}'""".format(userQllega.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                userRetur = UserN(row[0],row[1],UserN.check_password(row[2],userQllega.password),row[3],row[4])
                return userRetur
            else:
                return None
        except Exception as ex:
            raise Exception (ex)
        
    