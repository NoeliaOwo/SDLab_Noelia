"""Servant implementations for service discovery."""

import Ice

Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive


class Discovery(IceDrive.Discovery):
    """Servants class for service discovery."""
    
    def __init__(self):
        self.authentication_services = set()
        self.directory_services = set()
        self.blob_services = set()

    def announceAuthentication(self, prx: IceDrive.AuthenticationPrx, current: Ice.Current = None) -> None:
        """Receive an Authentication service announcement."""
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
        

        
        
    
    
