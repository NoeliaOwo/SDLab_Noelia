
import json
import Ice

class Persistencia:
    
    def __init__(self,archivo):
        self.archivo = archivo
        self.users = self.load_users()
        
    def load_users(self): 
        users = {}
        with open(self.archivo, 'r') as file:
            for username, password in list(json.load(file).items()):
                users[username] = password 
        return users
    
  
    def check_user(self, username, password):
        if username in self.users:
            if self.users[username] == password:
                return True
        return False
    
    
    def add_user(self, username, password):
        if not self.check_user(username, password):
                self.users[username] = password
                with open(self.archivo, 'w') as file:
                    json.dump(self.users, file)
                return True
        else:
            return False 
    
    def remove_user(self, username, password):
        if self.check_user(username, password):
            del self.users[username]
            with open(self.archivo, 'w') as file:
                json.dump(self.users, file)
                return True
        else:
            return False
    
    def update_user_password(self, username, password, new_password):
        if self.check_user(username, password):
            self.users[username] = new_password
            with open(self.archivo, 'w') as file:
                json.dump(self.users, file)
                        
                        
    def update_user_username(self, username, password, new_username):
        if self.check_user(username, password):
            if new_username in self.users:
                print(f"El nuevo nombre de usuario '{new_username}' ya existe.")
                return
            self.users[new_username] = self.users.pop(username) 
            with open(self.archivo, 'w') as file:
                json.dump(self.users, file)
       
                                     


  
    
p = Persistencia("pruebas.json")
p.remove_user("Noelia", "0123")
#p.update_user_username("paca", "juana", "xd")