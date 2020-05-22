from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token')
PAYLOAD = {'name':'Demo User', 'email':'test@test.com', 'password':'testpassword'}

def create_user(**params):
    user = get_user_model().objects.create_user(**params)
    return user

class PublicUserTokenApiTests(TestCase):
    """Base User Test class"""
    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """ Test that a toke is created for the user """             
        payload = PAYLOAD.copy()
        create_user(**payload)
        payload['username'] = payload['email']
        del payload['email']        
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test user for invalid credentials """        
        payload = PAYLOAD.copy()        
        create_user(**payload)
        payload['password'] = 'asdlfjalsdjfl@3242ljlsajdfl'

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_no_user(self):
        """Test that token is not created"""        
        res = self.client.post(TOKEN_URL, PAYLOAD)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_valid_user(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
 