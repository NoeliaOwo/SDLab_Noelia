import time
from tkinter import messagebox
from typing import List
import Ice
import sys

from icedrive_authentication.user import User


Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive

class ClientApp(Ice.Application):
    """Implementation of the Ice.Application for the Client service."""
    def __init__(self):
        self.user_id = {}
        
    def run(self, args: List[str]):
        
        my_adapter = self.communicator().createObjectAdapterWithEndpoints("MyAdapter", "default -p 0")
        base = self.communicator().stringToProxy("Authentication -t -e 1.1:tcp -h 127.0.0.1 -p 10000 -t 60000")
        authentication = IceDrive.AuthenticationPrx.checkedCast(base)
        
        try:
            while True:
                print("1. Crear usuario.\n2. Eliminar usuario.\n3. Iniciar sesión.\n4. Verificar usuario.\n5. Acceso con usuario externo.\n6. Comprobar si el usuario sigue vivo.\n7. Comprobar si el usuario sigue vivo después de 2 min.\n8. Obtener nombre de los usuarios logeados.\n9. Renovar validez de un usuario.\n10. Renovar falla.\n11. Salir.")
                option = input("Elige una opción: ")

                match option:
                    
                    case "1":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        self.user_id[username] = authentication.newUser(username, password)
                        print(f"Hemos creado al usuario {username}.\n")
                        
                    case "2":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        authentication.removeUser(username, password)
                        if username in self.user_id:
                            del self.user_id[username]
                        print(f"Hemos eliminado al usuario {username}.\n")    
                                          
                    case "3":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        self.user_id[username] = authentication.login(username, password)
                        print(f"El usuario {username} se ha logeado.\n")
                        
                    case "4":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        userproxy = self.user_id.get(username) # Busco el proxy del usuario
                        if userproxy is None:
                            print(f"El usuario {username} no se ha logeado.\n")
                        elif authentication.verifyUser(userproxy):
                            print(f"El usuario {username} está verificado.\n")
                        else:
                            print(f"El usuario {username} no está verificado.\n")
                            
                    case "5":
                        # Creación del usuario externo
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        user = User(username, password)
                        user_adapter = my_adapter.addWithUUID(user)
                        proxy = IceDrive.UserPrx.uncheckedCast(user_adapter)
                        
                        if authentication.verifyUser(proxy):
                            print(f"El usuario {username} está verificado.\n")
                        else:
                            print(f"El usuario {username} no está verificado.\n")
                            
                    case "6":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        proxy = self.user_id.get(username)
                        
                        if proxy is None:
                            print(f"El usuario {username} no está logeado.\n")
                        elif proxy.isAlive():
                            print(f"El usuario {username} está vivo.\n")
                        else:
                            print(f"El usuario {username} no está vivo.\n")
                            
                    case "7":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        proxy = self.user_id.get(username)
                        time.sleep(120)
                        
                        if proxy is None:
                            print(f"El usuario {username} no está logeado.\n")
                        elif proxy.isAlive():
                            print(f"El usuario {username} está vivo.\n")
                        else:
                            print(f"El usuario {username} no está vivo.\n")
                            
                    case "8":
                        print("Usuarios logeados: ")
                        for proxy in self.user_id.values():
                            print(f"{proxy.getUsername()}, ")
                            
                    case "9":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        proxy = self.user_id.get(username)
                        if proxy is None:
                            print(f"El usuario {username} no se ha logeado.\n")
                        else:
                            proxy.refresh()
                            print(f"Se ha renovado la validez del usuario {username}.\n")
                    
                    case "10":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        user = User(username, password)
                        user_adapter = my_adapter.addWithUUID(user)
                        proxy = IceDrive.UserPrx.uncheckedCast(user_adapter)
                        proxy.refresh()
                        print(f"Se ha renovado la validez del usuario {username}.\n")
                            
                    case "11":
                        break
                    case _:
                        print("Opción inválida")
        except Exception as e:
            print(f"{e}")
            return 0

        

def get_input_and_check(prompt):
    while True:
        value = input(prompt)
        if len(value) <= 10:
            return value
        print("El dato no puede exceder los 20 caracteres.")
        
        
def client():
    app = ClientApp()
    return app.main(sys.argv)
   
        
if __name__ == "__main__": 
    client()   
    
