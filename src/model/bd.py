class secretKEY:
    SECRET_KEY = 'asdasdasdsdf'

class bd (secretKEY):
    MYSQL_HOST = 'localhost:3306'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'appsalud'

configu = {
    'db':bd
}

