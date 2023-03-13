from werkzeug.security import check_password_hash
class UserN():
    def __init__(self,id,username,password,fullname = "") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname

    @classmethod
    def check_password (self,hashed_password,password_plana): 
        return check_password_hash(hashed_password,password_plana)
    
    
