from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# class UserRegistrationTest(TestCase):
#     def test_user_registration(self):
#         response = self.client.post(reverse('register'), {
#             'username': 'testuser',
#             'password1': 'strongpassword123',
#         })
#
#         # Проверяем успешную регистрацию (редирект на страницу логина)
#         self.assertEqual(response.status_code, 200)
#         self.assertRedirects(response, reverse('login'))
#
#         # Проверяем, что пользователь был создан в базе данных
#         user = User.objects.filter(username='testuser').exists()
#         self.assertTrue(user)

class UserLoginTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя в базе данных
        self.user = User.objects.create_user(username='testuser', password='strongpassword123')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'strongpassword123',
        })

        # Проверяем успешную авторизацию (редирект на главную страницу)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        # Проверяем, что пользователь залогинен
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class UserLoginFailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='strongpassword123')

    def test_user_login_fail(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        # Проверяем, что авторизация не удалась
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
