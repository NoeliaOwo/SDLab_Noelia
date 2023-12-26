
import time
import Ice
import sys
Ice.loadSlice('icedrive_authentication/ssdd.ice')
import SSDD

class Client (SSDD.Cristian):
    
    def getServerTime(dni:str, tc1, current: Ice.Current = None) -> str:
        #ts = tc1 + ((time.time() - tc1) / 2)
        ts = tc1 - time.time()
        return ts
    
class SyncReport (SSDD.SyncReport):
    
    def notifySync(dni:str, fullname, tc2, newTime, error, current: Ice.Current = None) -> None:
        print("SyncReport: " + dni + " " + fullname + " " + str(tc2) + " " + str(newTime) + " " + str(error))
        
             

class SyncClient(Ice.Application):
    def run(self, args):
        proxy = self.communicator().stringToProxy("Cristian -t -e 1.1:tcp -h 93.189.90.58 -p 4000 -t 60000")
        server = SSDD.CristianPrx.checkedCast(proxy)
        b = server.notifySync("06297500", "Noelia Diaz", time.time(), time.time(), False)
        a = server.getServerTime("06297500", time.time())
        print(a)
        
        
        
        
def main():
    app = SyncClient()
    return app.main(sys.argv)
        
if __name__ == "__main__": 
    main()