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


def main():
    """Handle the icedrive-authentication program."""
    app = AuthenticationApp()
    return app.main(sys.argv, "config/authentication.config")
  
if __name__ == "__main__": 
    main()

