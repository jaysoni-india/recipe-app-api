from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

def create_user(**params):
        user = get_user_model().objects.create_user(**params)
        return user

class UserTestSetup(TestCase):
    """User Test setup class"""
    def setUp(self):
        self.client = APIClient()        
        self.PAYLOAD = {'name':'Demo User', 'email':'test@test.com', 'password':'testpassword'}
        self.CREATE_USER_URL = reverse('user:create')
        self.TOKEN_URL = reverse('user:token')
