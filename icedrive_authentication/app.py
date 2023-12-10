"""Authentication service application."""

import logging
import sys
from typing import List

import Ice

from . import authentication


class AuthenticationApp(Ice.Application):
    """Implementation of the Ice.Application for the Authentication service."""

    def run(self, args: List[str]) -> int:
        """Execute the code for the AuthentacionApp class."""
        adapter = self.communicator().createObjectAdapter("AuthenticationAdapter")
        adapter.activate()

        servant = authentication.Authentication()
        servant_proxy = adapter.addWithUUID(servant)
        
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

