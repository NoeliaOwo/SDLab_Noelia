from typing import List
import uuid
import logging
import Ice
import sys


Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive

class ClientApp(Ice.Application):
    def run(self, args: List[str]):
        print(args[0])
        print("1")
        base = self.communicator().stringToProxy("Authentication -t -e 1.1:tcp -h 192.168.1.192 -p 10000 -t 60000")
        authentication = IceDrive.AuthenticationPrx.checkedCast(base)

       
        #a = authentication.newUser("Noelia", "0123")
        #print(a.getUsername())
        a = authentication.removeUser("Noeli", "0123")
        print(a.getUsername())
        
        return 0


def client():
    app = ClientApp()
    return app.main(sys.argv)
   
        
client()