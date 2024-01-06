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
from .delayed_response import AuthenticationQuery, AuthenticationQueryResponse
#from icedrive_authentication import authentication
import IceStorm
from .discovery import Discovery
from .persistence import Persistence


def anunciar(discovery_proxy, authentication):
    while True:
        discovery_proxy.announceAuthentication(IceDrive.AuthenticationPrx.uncheckedCast(authentication))
        time.sleep(5)  
        

class AuthenticationApp(Ice.Application):
    """Implementation of the Ice.Application for the Authentication service."""

    def run(self, args: List[str]) -> int:
        """Execute the code for the AuthentacionApp class."""
        persistencia = Persistence("client_testing/file.json")
        
        properties = self.communicator().getProperties()
        topic_name = properties.getProperty("DiscoveryTopic")
        topic_manager = IceStorm.TopicManagerPrx.checkedCast(self.communicator().propertyToProxy("IceStorm.TopicManager.Proxy"))
        
        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_manager.create(topic_name)
        
        
        adapter = self.communicator().createObjectAdapter("AuthenticationAdapter")
        adapter.activate()
        
        
        # Añado el servant Authentication al adapter
        authentication_servant = Authentication()
        authentication = adapter.addWithUUID(authentication_servant)
        authentication_proxy = IceDrive.AuthenticationPrx.checkedCast(authentication)
        

        
        # Añado el servant AuthenticationQuery al adapter
        authentication_query_servant = AuthenticationQuery()
        authentication_query = adapter.addWithUUID(authentication_query_servant)
        authentication_query_topic = topic.subscribeAndGetPublisher({},  authentication_query)
        authentication_query_proxy = IceDrive.AuthenticationQueryPrx.uncheckedCast(topic.getPublisher())
    
        #authentication_query_topic.getRequest()
        
        # Añado el servant Discovery al adapter
        discovery_servant = Discovery()
        discovery = adapter.addWithUUID(discovery_servant)
        discovery_topic = topic.subscribeAndGetPublisher({}, discovery)
        discovery_proxy = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())
        
        
        # Añado el servant AuthenticationQueryResponse al adapter
        authentication_query_response_servant = AuthenticationQueryResponse()
        authentication_query_response = adapter.addWithUUID(authentication_query_response_servant)
        authentication_query_response_proxy = IceDrive.AuthenticationQueryResponsePrx.uncheckedCast(topic.getPublisher())
        
        
        
        #threading.Thread(target=anunciar, args=(discovery_proxy, authentication), daemon=True).start()
        
        #if persistencia.check_user("Noelia", "1234"):
        #    authentication_proxy.login("Noelia","1234", None)
        #else:
        #    authentication_query_proxy.login("","", authentication_query_response_proxy)
        
        

    
        

        
        logging.info("Proxy: %s", authentication)
        
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


def main():
    """Handle the icedrive-authentication program."""
    app = AuthenticationApp()
    return app.main(sys.argv, "config/authentication.config")
  
if __name__ == "__main__": 
    main()

