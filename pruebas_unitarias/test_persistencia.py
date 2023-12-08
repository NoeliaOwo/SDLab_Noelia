import unittest
from unittest.mock import patch, mock_open
from icedrive_authentication.persistencia import Persistencia


class TestPersistencia(unittest.TestCase):
    
    # Load users
    @patch('builtins.open', new_callable=mock_open, read_data ='{"Ines": "1111"}')
    def test_load_users_another_persistencia(self, _):
        persistencia = Persistencia('fichero.json')
        self.assertTrue(persistencia.users, {"Ines": "1111"})
        self.assertNotIn("Miriam", persistencia.users)
           
    def test_load_users(self):
        persistencia = Persistencia('pruebas_unitarias/pruebas.json')
        self.assertEqual(persistencia.users, {"Samu": "1234", "Noe": "1234", "Ines": "1111"})
        self.assertNotIn("Miriam", persistencia.users)
      
    # Check user  
    @patch('builtins.open', new_callable=mock_open, read_data ='{"Ines": "1111"}')
    def test_check_user_another_persistencia(self, _):
        persistencia = Persistencia('fichero.json')
        self.assertTrue(persistencia.check_user("Ines", "1111"))
        self.assertFalse(persistencia.check_user("Pablo", "hola"))

    def test_check_user(self):
        persistencia = Persistencia('pruebas_unitarias/pruebas.json')
        self.assertTrue(persistencia.check_user("Ines", "1111"))
        self.assertFalse(persistencia.check_user("Pablo", "hola"))

    # Check user username
    def test_check_user_username(self):
        persistencia = Persistencia('pruebas_unitarias/pruebas.json')
        self.assertTrue(persistencia.check_user_username("Ines"))
        self.assertFalse(persistencia.check_user_username("Pablo"))
    # Check user password
    def test_check_user_password(self):
        persistencia = Persistencia('pruebas_unitarias/pruebas.json')
        self.assertTrue(persistencia.check_user_password("Ines", "1111"))
        self.assertFalse(persistencia.check_user_password("Samu", "hola"))
        
    # Add user
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_add_user(self, _):
        persistencia = Persistencia('fichero.json')
        self.assertTrue(persistencia.add_user("Miriam", "2222"))
        self.assertFalse(persistencia.add_user("Ines", "1111"))
    
    # Remove user  
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_remove_user_another_persistencia(self, _):
        persistencia = Persistencia('fichero.json')
        self.assertTrue(persistencia.remove_user("Ines", "1111"))
        self.assertFalse(persistencia.remove_user("Miriam", "2222"))

    # Update user password
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_update_user_password(self, _):
        persistencia = Persistencia('fichero.json')
        persistencia.update_user_password("Ines", "1111", "nueva_contrasena")
        self.assertEqual(persistencia.users["Ines"], "nueva_contrasena")

    # Update user username
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_update_user_username(self, _):
        persistencia = Persistencia('fichero.json')
        persistencia.update_user_username("Ines", "1111", "Maria")
        self.assertEqual(persistencia.users["Maria"], "1111")


if __name__ == '__main__':
    unittest.main()
