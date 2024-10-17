from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='testuser@example.com')

    def test_user_create(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password': 'newpassword123',
            'password_confirm': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешного создания
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)

    def test_user_update(self):
        response = self.client.post(reverse('user_update', args=[self.user.pk]), {
            'username': 'updateduser',
            'email': 'updateduser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_user_delete(self):
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertFalse(user_exists)
