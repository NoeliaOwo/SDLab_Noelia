import Ice
from .user import User
from .persistence import Persistence
from .delayed_response import AuthenticationQuery, AuthenticationQueryResponseLogin, AuthenticationQueryResponseNewUser

import IceStorm
import IceDrive


class Authentication(IceDrive.Authentication):
    
    def __init__(self, direccion: str, authentication_query_servant: AuthenticationQuery, topic: IceStorm.Topic):
        self.persistence = Persistence(direccion)
        self.user_identities = {} 
        self.authentication_query_servant = authentication_query_servant
        self.topic = topic
                       

    def login(self, username: str, password: str, current: Ice.Current = None)-> IceDrive.UserPrx:
        if self.persistence.check_user_password(username, password):
            return self.create_new_user_proxy(username, password, current)
        else:
            if self.persistence.check_user_username(username) and not self.persistence.check_user_password(username, password):
                raise IceDrive.Unauthorized()
            else:
                future = Ice.Future() 
                authentication_query_response_servant = AuthenticationQueryResponseLogin(future, IceDrive.Unauthorized()) 
                authentication_query_response_proxy = current.adapter.addWithUUID(authentication_query_response_servant)
                authentication_query_responseProxy = IceDrive.AuthenticationQueryResponsePrx.uncheckedCast(authentication_query_response_proxy)
                publiser = IceDrive.AuthenticationQueryPrx.uncheckedCast(self.topic.getPublisher())
                publiser.login(username, password, authentication_query_responseProxy)
                return future
       
       
    def newUser(self, username: str, password: str, current: Ice.Current = None) -> IceDrive.UserPrx:
        if self.persistence.check_user_password(username, password):
            raise IceDrive.UserAlreadyExists()
        else:  
            future = Ice.Future() 
            authentication_query_response_servant = AuthenticationQueryResponseNewUser(future, IceDrive.UserAlreadyExists()) 
            authentication_query_response_proxy = current.adapter.addWithUUID(authentication_query_response_servant)
            authentication_query_responseProxy = IceDrive.AuthenticationQueryResponsePrx.uncheckedCast(authentication_query_response_proxy)
            publiser = IceDrive.AuthenticationQueryPrx.uncheckedCast(self.topic.getPublisher())
            if publiser.doesUserExist(username, authentication_query_responseProxy):
                future.result()
            self.persistence.add_user(username, password)
            return self.create_new_user_proxy(username, password, current)
                
                
    def create_new_user_proxy(self, username: str, password: str, current: Ice.Current):
        user = User(username, password)
        proxy = current.adapter.addWithUUID(user)
        self.user_identities[username] = proxy.ice_getIdentity()
        return IceDrive.UserPrx.uncheckedCast(proxy)
    
    
    def print_user_ids(self):
        for key, value in self.user_identities.items():
            print(f'Key: {key}, Value: {value}')
                    
    
    def removeUser(self, username: str, password: str, current: Ice.Current = None) -> None:
        if self.persistence.remove_user(username, password):
            if username in self.user_identities:
                current.adapter.remove(self.user_identities.get(username))
                del self.user_identities[username]
        else:
            raise IceDrive.UserAlreadyExists()
    
          
    def verifyUser(self, userver , current: Ice.Current = None) -> bool:
        identity = userver.ice_getIdentity()
        if current.adapter.find(identity):
            return True
        else:
            return False
            


        
