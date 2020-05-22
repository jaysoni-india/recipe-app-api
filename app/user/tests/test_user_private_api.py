
from .user_private_test_setup import status, UserPrivateTestSetup

class PrivateUserApiTests(UserPrivateTestSetup):
    """Test API requests thata require authentication"""

    def test_retrieve_profile_success(self):
        """Test retirieving profile for logged in user"""        
        res = self.client.get(self.ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
             'name': self.user.name,
             'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that POST is nto allowed on the me url"""
        res = self.client.post(self.ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = self.PAYLOAD.copy()
        payload['name'] = 'New Name'
        payload['password'] = 'newpassword123'

        res = self.client.patch(self.ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


        



    
