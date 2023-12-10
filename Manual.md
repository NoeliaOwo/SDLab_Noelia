# IceDrive Authentication Service Guidelines
**Bienvenido al servicio Authentication!!! :D**

## Instalación
- Para poder utilizar nuestros servicios primero debe clonar nuestro repositorio de GitHub: git clone https://github.com/NoeliaOwo/SDLab_Noelia.git. 
- Luego, necesita instalar la aplicación en su dispositivo mediante: __pip install -e__ .
- A continuación, debe iniciar el servidor con el siguiente comando: __icedrive-authentication__.
- Finalmente, podrá conectarse como cliente utilizando: __icedrive-authentication-client__. También tiene disponible nuestra interfaz gráfica. Si prefiere usar está, ejecute: __icedrive-authentication-UIclient.__

## Aplicaciones
### Cliente

Tendrá disponible las siguientes opciones:
1. Iniciar sesión. Introduzca un nombre y contraseña. Debe introducir unas credenciales válidas, sino salta una excepción.
2. Crear usuario. Introduzca un nombre y constraseña para crear un usuario. Si introduce un nombre que ya se encuentra registrado, salta una excepción.
3. Eliminar usuario. Introduzca un nombre y contraseña para eliminar un usuario. Debe introducir unas creedenciales válidas, sino salta una excepción.
4. Verificar usuario. Introduzca un nombre de un usuario que se haya logeado o creado (al crear un usuario, se logea automáticamente). Informa si el usuario introducido es válido.
5. Acceso con usuario externo. Esta operación sirve para comprobar que verifyUser devuelve false cuando el objeto User es creado por otras aplicaciones (usuario inválido).
6. Obtener nombre de los usuarios logeados. Devuelve el nombre de los usuarios que han sido logeados.
7. Comprobar si el usuario sigue vivo. Introducir el nombre de un usuario logeado o creado. Sirve para comprobar la validez de las credenciales de un usuario. Al crear un usuario, sus credenciales tendrán una validez de 2 minutos. Después de dos minutos, sus credenciales serán inválido.
8. Comprobar si el usuario sigue vivo después de 2 min. Sirve para comprobar que las credenciales son inválidas después de dos minutos.
9. Renovar validez de un usuario. Introduzca un nombre de un usuario logeado o creado. Sirve para poder extender la validez de las credenciales de un usuario. 
10. Renovar (para comprobar excepciones). Introduzca un nombre y contraseña para crear un usuario. Sirve para comprobar las excepciones del método refresh. Si el usuario no existe o sus credenciales son inválidas, salta una excepción. También salta si pasan más de 2 min.
11. Salir. Para salir del programa

## Interfaz gráfica
Al iniciar la aplicación aparece una ventana con dos botones, uno para acceder a las funcionalidades de Authentication y otro para acceder a las de User.
Si pulsa Authentication, aparece una ventana con las siguientes opciones: Iniciar sesión, Crear usuario, Eliminar usuario, Verificar usuario y Acceso con usuario externo.
En el caso de que pulse User, aparece: Obtener nombre de los usuarios logeados, Comprobar si el usuario sigue vivo, Comprobar si el usuario sigue vivo después de 2 min, Renovar validez de un usuario, Renovar (para comprobar excepciones).

Espero que haya disfrutado nuestra aplicación <3

