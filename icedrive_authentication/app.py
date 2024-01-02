"""Authentication service application."""

import logging
import sys
import threading
import time
from typing import List

import Ice

from .discovery import Discovery

#Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive
from .authentication import Authentication
from .delayed_response import AuthenticationQueryResponse
#from icedrive_authentication import authentication
import IceStorm


def anunciar(proxy, servant_proxy):
    while True:
        proxy.announceAuthentication(IceDrive.AuthenticationPrx.uncheckedCast(servant_proxy))
        time.sleep(5)  
        

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
        discovery = Discovery()
        discovery_proxy = adapter.addWithUUID(discovery)
        proxy = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())
        
        topic.subscribeAndGetPublisher({}, discovery_proxy)
        threading.Thread(target=anunciar, args=(proxy, servant_proxy), daemon=True).start()
    
        
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

