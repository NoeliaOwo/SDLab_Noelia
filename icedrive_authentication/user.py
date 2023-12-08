#!/usr/bin/env python3

import time
import Ice

Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive


from icedrive_authentication import persistencia


class User(IceDrive.User):
    
    
    def __init__(self, username:str, password:str) -> None:
        self.username = username
        self.password = password
        self.last_time = time.time()
        

    def getUsername(self, current: Ice.Current = None) -> str:
        return self.username

    def isAlive(self, current: Ice.Current = None) -> bool:
        now = time.time()
        return now - self.last_time <= 120
    
    def get_persistencia(self):
        return persistencia.Persistencia("pruebas_cliente/pruebas.json")

    def refresh(self, current: Ice.Current = None) -> None:
        if self.get_persistencia().check_user_username(self.username):
            if self.get_persistencia().check_user_password(self.username, self.password):
                if self.isAlive():
                    self.last_time = time.time()
                else:
                    raise IceDrive.Unauthorized()
            else:
                raise IceDrive.Unauthorized()
        else:
            raise IceDrive.UserNotExist()

    def __str__(self) -> str:
        return print(self.username, self.password, self.last_time)


