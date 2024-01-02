
import Ice
from .user import User
from .persistence import Persistence


Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive

class Authentication(IceDrive.Authentication):
    
    def __init__(self):
        self.persistencia = Persistence("client_testing/file.json")
        self.user_identities = {} 
                       
 
    def login(self, username: str, password: str, current: Ice.Current = None)-> IceDrive.UserPrx:
        if not self.persistencia.check_user_password(username, password):
            raise IceDrive.Unauthorized()
        return self.create_new_user_proxy(username, password, current)
    

    def newUser(self, username: str, password: str, current: Ice.Current = None) -> IceDrive.UserPrx:
        if not self.persistencia.add_user(username, password):
            raise IceDrive.UserAlreadyExists()
        return self.create_new_user_proxy(username, password, current)
    
    
    def removeUser(self, username: str, password: str, current: Ice.Current = None) -> None:
        if not self.persistencia.remove_user(username, password):
            raise IceDrive.Unauthorized()
        if username in self.user_identities:
            current.adapter.remove(self.user_identities.get(username))
            del self.user_identities[username]
            
 
    def verifyUser(self, userver , current: Ice.Current = None) -> bool:
        identity = userver.ice_getIdentity()
        if current.adapter.find(identity):
            return True
        else:
            return False
    
    
    def create_new_user_proxy(self, username: str, password: str, current: Ice.Current):
        user = User(username, password)
        proxy = current.adapter.addWithUUID(user)
        self.user_identities[username] = proxy.ice_getIdentity()
        return IceDrive.UserPrx.uncheckedCast(proxy)
    
    
    def print_user_ids(self):
        for key, value in self.user_identities.items():
            print(f'Key: {key}, Value: {value}')
        
