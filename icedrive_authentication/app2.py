"""Authentication service application."""
import sys
import time
from typing import List

import Ice
import IceStorm
import IceDrive

from .discovery import Discovery
from .authentication import Authentication
from .delayed_response import AuthenticationQuery
from .persistence import Persistence


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
        
        
        discovery_servant = Discovery()
        discovery_proxy = adapter.addWithUUID(discovery_servant)
        discovery_topic = topic.subscribeAndGetPublisher({}, discovery_proxy)
        discovery_publisher = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())
        
  
        authentication_query_servant = AuthenticationQuery(Persistence(properties.getProperty("PersistenceFile2")))
        authetication_query_proxy = adapter.addWithUUID(authentication_query_servant)
        authentication_query_topic = topic.subscribeAndGetPublisher({}, authetication_query_proxy)
        
        authentication_servant = Authentication(properties.getProperty("PersistenceFile2"), authentication_query_servant, topic)
        authentication_proxy = adapter.addWithUUID(authentication_servant)
        

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0
    

def main():
    """Handle the icedrive-authentication program."""
    app = AuthenticationApp()
    return app.main(sys.argv, "config/authentication.config")
  
if __name__ == "__main__": 
    main()



