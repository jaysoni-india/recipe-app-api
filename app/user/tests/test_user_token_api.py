
from .user_test_setup import create_user, UserTestSetup, status, get_user_model

class PublicUserTokenApiTests(UserTestSetup):
    """Base User Test class"""  

    def test_create_token_for_user(self):
        """ Test that a token is created for the user """             
        payload = self.PAYLOAD.copy()
        create_user(**payload)
        payload['username'] = payload['email']
        del payload['email']        
        res = self.client.post(self.TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test user for invalid credentials """        
        payload = self.PAYLOAD.copy()        
        create_user(**payload)
        payload['password'] = 'asdlfjalsdjfl@3242ljlsajdfl'

        res = self.client.post(self.TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_no_user(self):
        """Test that token is not created"""        
        res = self.client.post(self.TOKEN_URL, self.PAYLOAD)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_valid_user(self):
        """Test that email and password are required"""
        res = self.client.post(self.TOKEN_URL, {'email': 'one', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
 