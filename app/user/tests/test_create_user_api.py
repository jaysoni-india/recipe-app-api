from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
payload = {'name':'Demo User', 'email':'test@test.com', 'password':'testpassword'}

def create_user(**params):
    user = get_user_model().objects.create_user(**params)
    return user

class PublicCreateUserApiTests(TestCase):
    """Base User Test class"""
    def setUp(self):
        self.client = APIClient()        
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""                    
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test user creation with already exists user"""
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must have greater than 5 character"""
        lpayload = payload
        lpayload['password'] = 'abcd'

        res = self.client.post(CREATE_USER_URL, lpayload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)    
  