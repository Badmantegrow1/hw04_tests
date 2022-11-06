from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='username')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_page_app_user_for_guest_client(self):
        """Проверяем URL's приложения users для неавторизованных
        пользователей"""
        urls_name = {
            '/auth/login/',
            '/auth/signup/',
            '/auth/password_reset/',
        }
        for address in urls_name:
            with self.subTest():
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_app_users_for_autorized_client(self):
        """Проверяем URL's приложения users для авторизованных
        пользователей"""
        urls_name = {
            '/auth/password_change/',
            '/auth/logout/',
        }
        for address in urls_name:
            with self.subTest():
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template_for_quest_client(self):
        """URL-адрес для неавторизованных пользователей использует
        соответствующий шаблон."""
        templates_urls_name = {
            'users/login.html': '/auth/login/',
            'users/signup.html': '/auth/signup/',
            'users/password_reset_form.html': '/auth/password_reset/',
        }
        for template, url in templates_urls_name.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_for_authorized_client(self):
        """URL-адрес для авторизованных пользователей использует
        соответствующий шаблон."""
        templates_urls_name = {
            'users/password_change_form.html': '/auth/password_change/',
            'users/logged_out.html': '/auth/logout/',
        }
        for template, url in templates_urls_name.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
