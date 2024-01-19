from typing import List
import Ice
import sys

Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive

class ClientApp(Ice.Application):
    def run(self, args: List[str]): 
        
        with open('authentication_proxy.txt', 'r') as f:
            line = f.readline()
            
        base = self.communicator().stringToProxy(line)
        authentication = IceDrive.AuthenticationPrx.uncheckedCast(base)
        a = authentication.login("Terry", "1234")
        print(a)
        
        return 0
    
    
def main():
    app = ClientApp()
    sys.exit(app.main(sys.argv))
    
if __name__ == "__main__":
    main()
                        