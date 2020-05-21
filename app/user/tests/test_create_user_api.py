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

    def test_user_password_strength(self):
        """Test password must have greater than 5 character"""
        payload = self.payload

        payload['password'] = 'abcd'

        res = self.client.post(self.CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
