import unittest
from unittest.mock import patch, mock_open
from icedrive_authentication.persistence import Persistence


class TestPersistence(unittest.TestCase):
    
    # Load users
    @patch('builtins.open', new_callable=mock_open, read_data ='{"Ines": "1111"}')
    def test_load_users_another_persistence(self, _):
        persistence = Persistence('file.json')
        self.assertTrue(persistence.users, {"Ines": "1111"})
        self.assertNotIn("Miriam", persistence.users)
           
    def test_load_users(self):
        persistence = Persistence('unit_testing/file.json')
        self.assertEqual(persistence.users, {"Samu": "1234", "Noe": "1234", "Ines": "1111"})
        self.assertNotIn("Miriam", persistence.users)
      
    # Check user  
    @patch('builtins.open', new_callable=mock_open, read_data ='{"Ines": "1111"}')
    def test_check_user_another_persistence(self, _):
        persistence = Persistence('file.json')
        self.assertTrue(persistence.check_user("Ines", "1111"))
        self.assertFalse(persistence.check_user("Pablo", "hola"))

    def test_check_user(self):
        persistence = Persistence('unit_testing/file.json')
        self.assertTrue(persistence.check_user("Ines", "1111"))
        self.assertFalse(persistence.check_user("Pablo", "hola"))

    # Check user username
    def test_check_user_username(self):
        persistence = Persistence('unit_testing/file.json')
        self.assertTrue(persistence.check_user_username("Ines"))
        self.assertFalse(persistence.check_user_username("Pablo"))
        
    # Check user password
    def test_check_user_password(self):
        persistence = Persistence('unit_testing/file.json')
        self.assertTrue(persistence.check_user_password("Ines", "1111"))
        self.assertFalse(persistence.check_user_password("Samu", "hola"))
        
    # Add user
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_add_user(self, _):
        persistence = Persistence('file.json')
        self.assertTrue(persistence.add_user("Miriam", "2222"))
        self.assertFalse(persistence.add_user("Ines", "1111"))
    
    # Remove user  
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_remove_user_another_persistence(self, _):
        persistence = Persistence('file.json')
        self.assertTrue(persistence.remove_user("Ines", "1111"))
        self.assertFalse(persistence.remove_user("Miriam", "2222"))

    # Update user password
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_update_user_password(self, _):
        persistence = Persistence('file.json')
        persistence.update_user_password("Ines", "1111", "new_password")
        self.assertEqual(persistence.users["Ines"], "new_password")

    # Update user username
    @patch('builtins.open', new_callable=mock_open, read_data='{"Ines": "1111"}')
    def test_update_user_username(self, _):
        persistence = Persistence('file.json')
        persistence.update_user_username("Ines", "1111", "Maria")
        self.assertEqual(persistence.users["Maria"], "1111")


if __name__ == '__main__':
    unittest.main()
