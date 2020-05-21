from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    user = get_user_model().objects.create_user(**params)
    return user

class PublicCreateUserApiTests(TestCase):
    """Test users API (public)"""
    def setUp(self):
        self.client = APIClient()
        self.payload = {'name':'Demo User', 'email':'test@test.com', 'password':'testpassword'}
        self.CREATE_USER_URL = reverse('user:create')
        self.TOKEN_URL = reverse('user:token')
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""        
        res = self.client.post(self.CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test user creation with already exists user"""
        create_user(**self.payload)

        res = self.client.post(self.CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must have greater than 5 character"""
        payload = self.payload

        payload['password'] = 'abcd'

        res = self.client.post(self.CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_for_user(self):
        """ Test that a toke is created for the user """
        payload = self.payload        
        create_user(**payload)
        payload['username'] = payload['email']
        del payload['email']        
        res = self.client.post(self.TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test user for invalid credentials """
        payload = self.payload
        create_user(**payload)
        payload['password'] = 'asdlfjalsdjfl@3242ljlsajdfl'

        res = self.client.post(self.TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_no_user(self):
        """Test that token is not created"""
        payload = self.payload
        res = self.client.post(self.TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_missing_valid_user(self):
        """Test that email and password are required"""
        res = self.client.post(self.TOKEN_URL, {'email': 'one', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




        
