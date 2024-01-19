"""Servant implementation for the delayed response mechanism."""
import threading
import Ice
import IceDrive
from .user import User
from .persistence import Persistence

        
class AuthenticationQueryResponseLogin(IceDrive.AuthenticationQueryResponse):
    """Query response receiver."""
    def __init__(self, future: Ice.Future, exception):
        self.promise = future
        self.future_exception = exception
        self.timer = threading.Timer(5.0, self.timeout)
        self.timer.start()

    def loginResponse(self, user: IceDrive.UserPrx, current: Ice.Current = None) -> None:
        """Receive an User when other service instance knows about it and credentials are correct."""
        self.promise.set_result(user)
        
    def userRemoved(self, current: Ice.Current = None) -> None:
        """Receive an invocation when other service instance knows the user and removed it."""
        
    def userExists(self, current: Ice.Current = None) -> None:
        """Receive an invocation when other service instance knows the user and removed it."""
        
    def verifyUserResponse(self, result: bool, current: Ice.Current = None) -> None:
        """Receive a boolean when other service instance is owner of the `user`."""
    
    def timeout(self):
        if not self.promise.done():
            self.promise.set_exception(self.future_exception)
    
            
class AuthenticationQueryResponseNewUser(IceDrive.AuthenticationQueryResponse):
    """Query response receiver."""
    def __init__(self, future: Ice.Future, exception):
        self.promise = future
        self.future_exception = exception
        self.timer = threading.Timer(5.0, self.userExists)
        self.timer.start()

    def loginResponse(self, user: IceDrive.UserPrx, current: Ice.Current = None) -> None:
        """Receive an User when other service instance knows about it and credentials are correct."""
        
    def userRemoved(self, current: Ice.Current = None) -> None:
        """Receive an invocation when other service instance knows the user and removed it."""

    def userExists(self, current: Ice.Current = None) -> None:
        """Receive an invocation when other service instance knows the user and removed it."""
        self.promise.set_exception(self.future_exception)
        
    def verifyUserResponse(self, result: bool, current: Ice.Current = None) -> None:
        """Receive a boolean when other service instance is owner of the `user`."""
        
    def timeout(self):
        """Receive an invocation when other service instance knows the user and removed it."""


class AuthenticationQuery(IceDrive.AuthenticationQuery):
    
    def __init__(self, persistence: Persistence):
        self.persistence = persistence
        
    """Query receiver."""
    def login(self, username: str, password: str, response: IceDrive.AuthenticationQueryResponsePrx, current: Ice.Current = None) -> None:
        """Receive a query about an user login."""
        if self.persistence.check_user_password(username, password):
            response.loginResponse(IceDrive.UserPrx.uncheckedCast(current.adapter.addWithUUID(User(username, password))))
   
    def doesUserExist(self, username: str, response: IceDrive.AuthenticationQueryResponsePrx, current: Ice.Current = None) -> None:
        """Receive a query about an user existence."""
        if self.persistence.check_user_username(username):
            response.userExists()

    def removeUser(self, username: str, password: str, response: IceDrive.AuthenticationQueryResponsePrx, current: Ice.Current = None) -> None:
        """Receive a query about an user to be removed."""
       
    def verifyUser(self, user: IceDrive.UserPrx, response: IceDrive.AuthenticationQueryResponsePrx, current: Ice.Current = None) -> None:
        """Receive a query about an `User` to be verified."""

        
        
   