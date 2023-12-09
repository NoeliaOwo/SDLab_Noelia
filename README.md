# IceDrive Authentication service guidelines
**Bienvenido al servicio Authentication!!! :D**

Para poder utilizar nuestros servicios necesita instalarse la aplicación en su dispositivo mediante: pip install -e .

A continuación, debe iniciar el servidor con el siguiente comando: icedrive-authentication-server

Finalmente, podrá conectarse como cliente utilizando: icedrive-authentication-client. También tiene disponible nuestra interfaz gráfica. Si prefiere usar esta, ejecute: icedrive-authentication-UIclient


Tiene un diccionario que almacena las identidades de los objetos User. 
Tendrá disponible varias opciones:
1. Crear usuario. Introduzca un nombre y constraseña para crear un usuario. Si introduce un nombre que ya se encuentra registrado, salta una excepción.
2. Eliminar usuario. Introduzca un nombre y contraseña para eliminar un usuario. Debe introducir unas creedenciales válidas, sino salta una excepción.
3. Iniciar sesión. Introduzca un nombre y contraseña. Debe introducir unas credenciales válidas, sino salta una excepción.
4. Verificar usuario. Introduzca un nombre de un usuario que se haya logeado o 
5. Acceso con usuario externo. Esta operación sirve para comprobar que verificar devuelve false cuando el objeto User es creado por otra aplicaciones.
6. Comprobar si el usuario sigue vivo.
7. Comprobar si el usuario sigue vivo después de 2 min.
8. Obtener nombre de los usuarios logeados.
9. Renovar validez de un usuario. Introduzca un nombre. 
10. Renovar (para comprobar excepciones). Introduzca un nombre y contraseña para crear un usuario. Sirve para comprobar las excepciones.
11. Salir.


Aparece una ventana con dos botones, uno para acceder a los métodos de Authenticator y otro para acceder a los métodos 

