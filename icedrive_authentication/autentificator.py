
import Ice

from icedrive_authentication.user import User


from . import persistencia


Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive

class Authentication(IceDrive.Authentication):
    
    def __init__(self):
        self.persistencia = persistencia.Persistencia("icedrive_authentication/pruebas.json")
              
 
    def login(self, username: str, password: str, current: Ice.Current = None)-> IceDrive.UserPrx:
        if self.persistencia.check_user(username, password):
            self.persistencia.add_user(username, password)
        else:
            raise IceDrive.Unauthorized


    def newUser(self, username: str, password: str, current: Ice.Current = None) -> IceDrive.UserPrx:
        if not self.persistencia.add_user(username, password):
            raise IceDrive.UserAlreadyExists()
        
        user = User(username, password)
        proxy = current.adapter.addWithUUID(user)
        return IceDrive.UserPrx.uncheckedCast(proxy)
    
            
    def removeUser(self, username: str, password: str, current: Ice.Current = None) -> None:
        if self.persistencia.remove_user(username, password):
            raise IceDrive.UserNotExist()
        
            
        
        user = User(username, password)
        current.adapter.remove(user)
        
                    
    # DUDAS               
    def verifyUser(self, userver:str , current: Ice.Current = None) -> bool:
        for user in self.users:
            if user.getUsername() == userver.username and user.password == userver.password:
                return True
        return False


