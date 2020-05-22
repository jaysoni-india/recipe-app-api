
from .user_test_setup import UserTestSetup,create_user, reverse, status

class UserPrivateTestSetup(UserTestSetup):
    """Test setup class for request that require authentication"""

    def setUp(self):
        super().setUp()        
        self.user = create_user(**self.PAYLOAD)
        self.client.force_authenticate(user=self.user)
        self.ME_URL = reverse('user:me')