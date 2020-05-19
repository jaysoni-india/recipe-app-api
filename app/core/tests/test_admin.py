from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@admin.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='pass123',
            name='Test userfullname'            
        )
    
    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # assertcontains check status is 200 and content contains string
        self.assertContains(res, self.user.name) 
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/{id}
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertTrue(res.status_code, 200)

        












