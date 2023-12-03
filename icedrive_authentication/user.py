#!/usr/bin/env python3

import time
import Ice
import IceDrive

class User(IceDrive.User):
    
    def __init__(self, username:str, password:str) -> None:
        self.username = username
        self.password=password
        self.last_time= time.time()

    def getUsername(self, current: Ice.Current = None) -> str:
        return self.username

    def isAlive(self, current: Ice.Current = None) -> bool:
        now = time.time()
        return now - self.last_time <= 120

    def refresh(self, current: Ice.Current = None) -> None:
        try:
            if self.username and self.password:
                self.last_time = time.time()
            else:
                raise Ice.UserNotExist
        except Ice.Unauthorized as e:
            print(f"Error: {e.reason}")
    # DUDAS

    def __str__(self) -> str:
        return print(self.username, self.password, self.last_time)


