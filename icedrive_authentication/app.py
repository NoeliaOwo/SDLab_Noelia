"""Authentication service application."""

import logging
import sys
import threading
import time
from typing import List

import Ice

Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive
from authentication import Authentication
#from icedrive_authentication import authentication
import IceStorm


def anunciar(proxy, servant):
    while True:
        proxy.announceAuthentication(IceDrive.AuthenticationPrx.uncheckedCast(servant))
        print("Anunciado")
        time.sleep(5)  

def escuchar():
    while True:
        
        time.sleep(1)  

class AuthenticationApp(Ice.Application):
    """Implementation of the Ice.Application for the Authentication service."""

    def run(self, args: List[str]) -> int:
        """Execute the code for the AuthentacionApp class."""
        properties = self.communicator().getProperties()
        topic_name = properties.getProperty("DiscoveryTopic")
        topic_manager = IceStorm.TopicManagerPrx.checkedCast(self.communicator().propertyToProxy("IceStorm.TopicManager.Proxy"))
        
        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_manager.create(topic_name)
        
        
        adapter = self.communicator().createObjectAdapter("AuthenticationAdapter")
        adapter.activate()
        servant = Authentication()
        servant_proxy = adapter.addWithUUID(servant)
        
        proxy = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())
        print(topic.getPublisher())
        
        #servant_proxy = IceDrive.AuthenticationPrx.uncheckedCast(topic.getPublisher())
        proxy.announceAuthentication(IceDrive.AuthenticationPrx.uncheckedCast(servant_proxy))
        
        # hago dos hilos uno para anunciarme cada 5 segundos y otro para escuchar y añadir los servicios a mi set de proxys de cada servicio
        #threading.Thread(target=anunciar, args=(proxy, servant_proxy), daemon=True).start()
        #threading.Thread(target=anunciar(proxy, servant_proxy), daemon=True).start()
        #threading.Thread(target=escuchar(), daemon=True).start()
        
        with open('server_proxy.txt', 'w') as f:
            f.write(str(servant_proxy))
        
        logging.info("Proxy: %s", servant_proxy)
        
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0
 
class Eamen:       
 def getProxy(self):
     print("hola")
     
     
class Discovery(IceDrive.Discovery):
    """Servants class for service discovery."""
    
    def __init__(self):
        self.authentication_services = set()
        self.directory_services = set()
        self.blob_services = set()

    def announceAuthentication(self, prx: IceDrive.AuthenticationPrx, current: Ice.Current = None) -> None:
        """Receive an Authentication service announcement."""
        
        print("puta")
        self.authentication_services.add(prx)
        print(prx)
        
    def announceDirectoryServicey(self, prx: IceDrive.DirectoryServicePrx, current: Ice.Current = None) -> None:
        """Receive an Directory service announcement."""
        self.directory_services.add(prx)
        print(prx)

    def announceBlobService(self, prx: IceDrive.BlobServicePrx, current: Ice.Current = None) -> None:
        """Receive an Blob service announcement."""
        self.blob_services.add(prx)
        print(prx)


def main():
    """Handle the icedrive-authentication program."""
    app = AuthenticationApp()
    return app.main(sys.argv, "config/authentication.config")
  
if __name__ == "__main__": 
    main()

