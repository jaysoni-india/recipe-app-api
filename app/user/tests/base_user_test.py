from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


class BaseUserTest(TestCase):
    """Base User Test class """
    def setUp(self):
        self.client = APIClient()
        self.status = status
        self.payload = {'name':'Demo User', 'email':'test@test.com', 'password':'testpassword'}
        self.CREATE_USER_URL = reverse('user:create')
        self.TOKEN_URL = reverse('user:token')

    def create_user(self, **params):
        user = self.get_user_model().objects.create_user(**params)
        return user

    def get_user_model(self):
        return get_user_model
        

        