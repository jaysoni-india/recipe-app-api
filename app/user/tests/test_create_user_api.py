from .user_test_setup import get_user_model, status, UserTestSetup, create_user

class PublicCreateUserApiTests(UserTestSetup):
    """Base User Test class"""                 
    
    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""                    
        res = self.client.post(self.CREATE_USER_URL, self.PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.PAYLOAD['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test user creation with already exists user"""
        create_user(**self.PAYLOAD)

        res = self.client.post(self.CREATE_USER_URL, self.PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password must have greater than 5 character"""
        lpayload = self.PAYLOAD
        lpayload['password'] = 'abcd'

        res = self.client.post(self.CREATE_USER_URL, lpayload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)    
  