import time
from typing import List
import Ice
import sys

from icedrive_authentication.user import User


Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive

class ClientApp(Ice.Application):
    """Implementation of the Ice.Application for the Client service."""
    def __init__(self):
        self.user_identities = {}
        
    def run(self, args: List[str]): 
        my_adapter = self.communicator().createObjectAdapterWithEndpoints("MyAdapter", "default -p 0")
        with open('server_proxy.txt', 'r') as f:
            line = f.readline()
        base = self.communicator().stringToProxy(line)
        authentication = IceDrive.AuthenticationPrx.checkedCast(base)
        
        try:
            while True:
                print("1. Iniciar sesión.\n2. Crear usuario.\n3. Eliminar usuario.\n4. Verificar usuario.\n5. Acceso con usuario externo.\n6. Obtener nombre de los usuarios logeados.\n7. Comprobar si el usuario sigue vivo.\n8. Comprobar si el usuario sigue vivo después de 2 min.\n9. Renovar validez de un usuario.\n10. Renovar (para comprobar excepciones).\n11. Salir.")
                option = input("Elige una opción: ")

                match option:
                    # LOGIN   
                    # 1. Un cliente puede hacer "login" con credenciales válidas y un UserPrx es devuelto.
                    # 2. Un cliente con credenciales inválidas al hacer "login" es rechazado.                          
                    case "1":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        self.user_identities[username] = authentication.login(username, password)
                        print(f"El usuario {username} se ha logeado.\n")
                        
                    # NEW USER
                    # 3. Un cliente puede registrarse con "newUser" y un UserPrx es devuelto.
                    # 4. Un cliente no puede registrarse si el nombre de usuario ya existe.
                    case "2":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        self.user_identities[username] = authentication.newUser(username, password)
                        print(f"Hemos creado al usuario {username}.\n")
                        
                    # REMOVE USER
                    # 5. Un cliente puede eliminar su usuario con "removeUser".
                    # 6. UN cliente no puede borrar un usuario sin aportar las credenciales correctas.
                    case "3":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        authentication.removeUser(username, password)
                        if username in self.user_identities:
                            del self.user_identities[username]
                        print(f"Hemos eliminado al usuario {username}.\n")
                    
                    # VERIFY USER
                    # 7. El método "verifyUser" devuelve verdadero para un UserPrx creado a través de "login" o "newUser".
                    case "4":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        user_proxy = self.user_identities.get(username) # Busco el proxy del usuario
                        if user_proxy is None:
                            print(f"El usuario {username} no se ha logeado.\n")
                        elif authentication.verifyUser(user_proxy):
                            print(f"El usuario {username} está verificado.\n")
                        else:
                            print(f"El usuario {username} no está verificado.\n")
                          
                    # VERIFY USER  
                    # 8. El método "verifyUser" devuelve falso para cualquier UserPrx, accseible o no, que no pertenezca a éste servcio.
                    case "5":
                        # Creación de un usuario externo
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        password = get_input_and_check("Introduce la contraseña: ")
                        user = User(username, password)
                        user_adapter = my_adapter.addWithUUID(user)
                        proxy = IceDrive.UserPrx.uncheckedCast(user_adapter)
                        
                        if authentication.verifyUser(proxy):
                            print(f"El usuario {username} está verificado.\n")
                        else:
                            print(f"El usuario {username} no está verificado.\n")
                    
                    # GET USERNAME
                    # 9. El método "getUsername" de UserPrx devuelve el nombre del usuario esperado
                    # En este caso, devuelve el nombre de todos los usuarios logeados o creados (al crearse se logea automáticamente).
                    case "6":
                        print("Usuarios logeados: ")
                        usernames = ""
                        for proxy in self.user_identities.values():
                            usernames += proxy.getUsername() + ", "
                        print(usernames[:-2] + "\n")
                    
                    # IS ALIVE
                    # 10. El método "isAlive" de UserPrx devuelve verdadero si han pasado menos de 2 minutos de su creación o del último "refresh".
                    case "7":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        proxy = self.user_identities.get(username)
                        
                        if proxy is None:
                            print(f"El usuario {username} no está logeado.\n")
                        elif proxy.isAlive():
                            print(f"El usuario {username} está vivo.\n")
                        else:
                            print(f"El usuario {username} no está vivo.\n")
                            
                    # IS ALIVE
                    # 11. El método "isAlive" de UserPrx devuelve falso si han pasado más de 2 minutos de su creación o del último "refresh".
                    # En este caso, espera 130 segundos para comprobar que el usuario no está vivo.
                    case "8":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        proxy = self.user_identities.get(username)
                        time.sleep(130)
                        
                        if proxy is None:
                            print(f"El usuario {username} no está logeado.\n")
                        elif proxy.isAlive():
                            print(f"El usuario {username} está vivo.\n")
                        else:
                            print(f"El usuario {username} no está vivo.\n")
                            
                    # REFRESH
                    # 12. El método "refresh" extiende la duración de las credenciales en 2 minutos.
                    # 15. El método "refresh" falla con Unauthorized si han pasado más de 2 minutos del último "refresh", por tanto no se puede renovar.
                    case "9":
                        username = get_input_and_check("Introduce el nombre de usuario: ")
                        proxy = self.user_identities.get(username)
                        if proxy is None:
                            print(f"El usuario {username} no se ha logeado.\n")
                        else:
                            proxy.refresh()
                            print(f"Se ha renovado la validez del usuario {username}.\n")
                    
                    # REFRESH
                    # Para probar que salta UserNotExist para usuarios que no existen y que salta Unauthorized para credenciales inválidas.
                    # Anteriormente se ha comprobado que funcionase para usuarios logeados (existen y sus credenciales son válidas).
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
                        print("Opción inválida.\n")
                        
        except Exception as e:
            print(f"{e}")
            return 0


def get_input_and_check(prompt):
    while True:
        value = input(prompt)
        if len(value) <= 10:
            return value
        print("El dato no puede exceder los 10 caracteres.")
        
        
def client():
    app = ClientApp()
    return app.main(sys.argv)
   
        
    
