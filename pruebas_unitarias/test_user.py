import time
import unittest
import Ice
from unittest.mock import MagicMock, mock_open, patch

from icedrive_authentication.user import User

Ice.loadSlice('icedrive_authentication/icedrive.ice')
import IceDrive
        
class TestUser(unittest.TestCase):
    def setUp(self):
        self.username = "Noe"
        self.password = "1234"
        self.time = time.time()
        self.user = User(self.username, self.password)
        
    def test_username(self):
        self.assertEqual(self.user.username, "Noe")
    
    def test_username_returns_incorrect_username(self):
        self.assertNotEqual(self.user.username, "Pedro")
        
    def test_password(self):
        self.assertEqual(self.user.password, "1234") 
        
    def test_username_returns_incorrect_password(self):
        self.assertNotEqual(self.user.password, "2345")

    def test_getUsername(self):
        self.assertEqual(self.user.getUsername(), self.username)
        
    def test_getUsername_returns_incorrect_username(self):
        self.assertNotEqual(self.user.getUsername(), "Pedro")

    def test_isAlive(self):
        self.assertTrue(self.user.isAlive())
        
    def test_isAlive_after_some_time(self):
        time.sleep(2)
        self.assertTrue(self.user.isAlive())
        
    def test_isAlive_after_many_time(self):
        time.sleep(130)  
        self.assertFalse(self.user.isAlive())
        
    def test_refresh(self):
        persistencia = MagicMock()
        persistencia.check_user_username.return_value = True
        persistencia.check_user_password.return_value = True
        self.user.get_persistencia = MagicMock(return_value=persistencia)
        self.user.refresh()
        self.assertTrue(self.user.isAlive())

    def test_refresh_unauthorized(self):
        persistencia = MagicMock()
        persistencia.check_user_username.return_value = True
        persistencia.check_user_password.return_value = False
        self.user.get_persistencia = MagicMock(return_value=persistencia)
        with self.assertRaises(IceDrive.Unauthorized):
            self.user.refresh()
            
    def test_refresh_user_not_exist(self):
        persistencia = MagicMock()
        persistencia.check_user_username.return_value = False
        self.user.get_persistencia = MagicMock(return_value=persistencia)
        with self.assertRaises(IceDrive.UserNotExist):
            self.user.refresh()
    
    @patch('builtins.open', new_callable=mock_open, read_data ='{"Noe": "1234"}')
    def test_refresh_updates_last_time(self, _):
        old_last_time = self.user.last_time
        self.user.refresh()
        self.assertNotEqual(self.user.last_time, old_last_time)

if __name__ == '__main__':
    unittest.main()