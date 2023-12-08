import sys
import time
from tkinter import Tk, Label, Button, Toplevel, font, Entry
import Ice 
from icedrive_authentication.user import User

Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive


class ClientApp(Ice.Application):
    def run(self, args):
        self.window = Tk()
        self.window.title("Cliente IceDrive")
        self.user_id = {}

        label_font = font.Font(family='Helvetica', size=16, weight='bold')
        self.label = Label(self.window, text="Bienvenido al Authenticator", font=label_font)
        self.label.pack(pady=10)

        window_width = 600
        window_height = 150
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.window.resizable(width=False, height=False)
        
        my_adapter = self.communicator().createObjectAdapterWithEndpoints("MyAdapter", "default -p 0")
        base = self.communicator().stringToProxy("Authentication -t -e 1.1:tcp -h 127.0.0.1 -p 10000 -t 60000")
        authentication = IceDrive.AuthenticationPrx.checkedCast(base)

        self.showUserDataButton = Button(self.window, text="Authentication", command = lambda: self.show_authentication_data(authentication, my_adapter))
        self.showUserDataButton.pack(pady=5)

        self.sayHelloButton = Button(self.window, text="User", command = lambda: self.show_user_data(my_adapter))
        self.sayHelloButton.pack(pady=5)


        self.window.mainloop()
        
        
    def show_authentication_data(self, authentication, my_adapter): 
        new_window = Toplevel(self.window)
        new_window.title("Authentication")
        new_window.resizable(False, False)

        label_font = font.Font(family='Helvetica', size=16, weight='bold')
        label = Label(new_window, text="Bienvenido a Authentication", font=label_font)
        label.pack(pady=10)
    
        window_width = 600
        window_height = 320
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        new_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        new_window.resizable(width=False, height=False)

        create_user_button = Button(new_window, text="Crear Usuario", command=lambda: self.create_user(authentication))
        create_user_button.pack(pady=5)

        remove_user_button = Button(new_window, text="Eliminar Usuario", command=lambda: self.remove_user(authentication))
        remove_user_button.pack(pady=5)

        login_button = Button(new_window, text="Iniciar Sesión", command= lambda: self.login_user(authentication))
        login_button.pack(pady=5)
        
        verify_user_button = Button(new_window, text="Verificar Usuario", command= lambda: self.verify_user(authentication))
        verify_user_button.pack(pady=5)
        
        verify_user_button = Button(new_window, text="Verificar Usuario Externo", command= lambda: self.verify_external_user(authentication, my_adapter))
        verify_user_button.pack(pady=5)
        
        new_window.mainloop()


    def create_user(self, authentication):
        new_window = Toplevel(self.window)
        new_window.title("Crear Usuario")
        new_window.resizable(False, False) 
        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()

        Label(new_window, text="Contraseña:").pack()
        password_entry = Entry(new_window)
        password_entry.pack()

        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Crear", command=lambda: self.create_user_action(username_entry.get(), password_entry.get(), authentication, success_label)).pack(pady=10)

        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))


    def create_user_action(self, username, password, authentication, success_label):
        try:
            self.user_id[username] = authentication.newUser(username, password)
            success_label.config(text=f"El usuario {username} ha sido creado!!")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")
        
        
    def remove_user(self, authentication):
        new_window = Toplevel(self.window)
        new_window.title("Eliminar Usuario")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        Label(new_window, text="Contraseña:").pack()
        password_entry = Entry(new_window)
        password_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Eliminar", command=lambda: self.remove_user_action(username_entry.get(), password_entry.get(), authentication, success_label)).pack(pady=10)
        
        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))


    def remove_user_action(self, username, password, authentication, success_label):
        try:
            authentication.removeUser(username, password)
            if username in self.user_id:
                del self.user_id[username]
            success_label.config(text=f"El usuario {username} ha sido eliminado :(")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")


    def login_user(self, authentication):
        new_window = Toplevel(self.window)
        new_window.title("Autentificar Usuario")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        Label(new_window, text="Contraseña:").pack()
        password_entry = Entry(new_window, show="*")
        password_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Login", command=lambda: self.login_user_action(username_entry.get(), password_entry.get(), authentication, success_label)).pack()
        
        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
       
        
    def login_user_action(self, username, password, authentication, success_label):
        try:
            self.user_id[username] = authentication.login(username, password)
            success_label.config(text=f"El usuario {username} está autorizado!!")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")


    def verify_user(self, authentication):
        new_window = Toplevel(self.window)
        new_window.title("Verificar Usuario")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Verificar", command=lambda: self.verify_user_action(username_entry.get(), authentication, success_label)).pack()
        
        new_window.geometry("200x150")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
        
        
    def verify_user_action(self, username, authentication, success_label):
        userproxy = self.user_id.get(username)
        if userproxy is None:
            success_label.config(text=f"El usuario {username} no sea logeado.")
        elif authentication.verifyUser(userproxy):
            success_label.config(text=f"El usuario {username} está verificado.")
        else:
            success_label.config(text=f"El usuario {username} no está verificado.")
            
            
    def verify_external_user(self, authentication, my_adapter):
        new_window = Toplevel(self.window)
        new_window.title("Verificar Usuario Externo")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        Label(new_window, text="Contraseña:").pack()
        password_entry = Entry(new_window)
        password_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Verificar", command=lambda: self.verify_external_user_action(username_entry.get(), password_entry.get(), authentication, my_adapter, success_label)).pack()
        
        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
        
            
    def verify_external_user_action(self, username, password, authentication, my_adapter, success_label):
        user = User(username, password)
        user_adapter = my_adapter.addWithUUID(user)
        proxy = IceDrive.UserPrx.uncheckedCast(user_adapter)
                        
        if authentication.verifyUser(proxy):
            success_label.config(text=f"El usuario {username} está verificado.")
        else:
            success_label.config(text=f"El usuario {username} no está verificado.")
            
    def show_user_data(self, my_adapter):
        new_window = Toplevel(self.window)
        new_window.title("User")
        new_window.resizable(False, False)

        label_font = font.Font(family='Helvetica', size=16, weight='bold')
        label = Label(new_window, text="Bienvenido a User", font=label_font)
        label.pack(pady=10)
    
        window_width = 600
        window_height = 320
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        new_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        new_window.resizable(width=False, height=False)

        create_user_button = Button(new_window, text="Sigue vivo", command=lambda: self.isAlive_user())
        create_user_button.pack(pady=5)

        remove_user_button = Button(new_window, text="No sigue vivo después de 2 min", command=lambda: self.isAlive_2min_user())
        remove_user_button.pack(pady=5)

        login_button = Button(new_window, text="Usuarios logeados", command= lambda: self.get_usernames())
        login_button.pack(pady=5)
        
        verify_user_button = Button(new_window, text="Renovar validez", command= lambda: self.extend_validity())
        verify_user_button.pack(pady=5)
        
        verify_user_button = Button(new_window, text="Renovar falla", command= lambda: self.extend_validity_error(my_adapter))
        verify_user_button.pack(pady=5)
        
        new_window.mainloop()
        
                            
    def extend_validity(self):
        new_window = Toplevel(self.window)
        new_window.title("Extender Validez del Usuario")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Extender Validez", command=lambda: self.extend_validity_action(username_entry.get(), success_label)).pack()
        
        new_window.geometry("300x300")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
        

    def extend_validity_action(self, username, success_label):
        try:
            proxy = self.user_id.get(username)
            if proxy is None:
                success_label.config(text=f"El usuario {username} no se ha logeado.\n")
            else:
                proxy.refresh()
                success_label.config(text=f"Se ha renovado la validez del usuario {username}.")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")
            
    
    def extend_validity_error(self, my_adapter):
        new_window = Toplevel(self.window)
        new_window.title("Extender Validez Error")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        Label(new_window, text="Contraseña:").pack()
        password_entry = Entry(new_window)
        password_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Extender Validez", command=lambda: self.extend_validity_error_action(username_entry.get(), password_entry.get(), my_adapter, success_label)).pack()
        
        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
        

    def extend_validity_error_action(self, username, password, my_adapter, success_label):
        try:
            user = User(username, password)
            user_adapter = my_adapter.addWithUUID(user)
            proxy = IceDrive.UserPrx.uncheckedCast(user_adapter)
            proxy.refresh()
            success_label.config(text=f"Se ha renovado la validez del usuario {username}.")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")
            
            
    def isAlive_user(self):
        new_window = Toplevel(self.window)
        new_window.title("Usuario Vivo")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
            
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Sigue Vivo", command=lambda: self.isAlive_action(username_entry.get(), success_label)).pack()

        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
        
        
    def isAlive_action(self, username, success_label):
        try:
            proxy = self.user_id.get(username)
            if proxy is None:
                success_label.config(text=f"El usuario {username} no se ha logeado.\n")
            elif proxy.isAlive():
                success_label.config(text=f"El usuario {username} está vivo.")
            else:
                success_label.config(text=f"El usuario {username} no está vivo.")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")
            
            
    def isAlive_2min_user(self):
        new_window = Toplevel(self.window)
        new_window.title("Usuario Vivo")
        new_window.resizable(False, False) 

        Label(new_window, text="Nombre de usuario:").pack()
        username_entry = Entry(new_window)
        username_entry.pack()
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Sigue Vivo", command=lambda: self.isAlive_2min_action(username_entry.get(), success_label)).pack()
        
        
        new_window.geometry("300x200")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
        
        
    def isAlive_2min_action(self, username, success_label):
        try:
            proxy = self.user_id.get(username)
            time.sleep(120)
            if proxy is None:
                success_label.config(text=f"El usuario {username} no se ha logeado.\n")
            elif proxy.isAlive():
                success_label.config(text=f"El usuario {username} está vivo.")
            else:
                success_label.config(text=f"El usuario {username} no está vivo.")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")
            
    def get_usernames(self):
        new_window = Toplevel(self.window)
        new_window.title("Usuarios Logeados")
        new_window.resizable(False, False) 
        
        success_label = Label(new_window, text="")
        success_label.pack()

        Button(new_window, text="Imprimir", command=lambda: self.get_usernames_action(success_label)).pack()
    
        
        new_window.geometry("500x100")
        new_window.geometry("+{}+{}".format(self.window.winfo_rootx(), self.window.winfo_rooty()))
            
            
    def get_usernames_action(self, success_label):
        try:
            usernames = ""
            for proxy in self.user_id.values():
                usernames += f"{proxy.getUsername()}, "
            success_label.config(text=f"{usernames}")
        except Exception as e:
            success_label.config(text=f"Error: {str(e)}")


def client():
    app = ClientApp()
    return app.main(sys.argv)


if __name__ == "__main__":
    client()