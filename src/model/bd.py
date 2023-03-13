class secretKEY:
    SECRET_KEY = 'asdasdasdsdf'
class bd (secretKEY):
    MYSQL_HOST = 'localhost:3306'
    MYSQL_USER = 'root'
   
    MYSQL_DB = 'mydb'

config = {
    'db':bd
}

