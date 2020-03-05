from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.test import TestCase
from django.urls import resolve, reverse

from users.forms import CustomUserCreationForm
from users.models import CustomUser
from users.views import SignUpView


class SignUpTests(TestCase):
    def setUp(self):
        data = {
            'username': 'john',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        url = reverse('signup')
        self.response = self.client.get(url)
        self.redirected_url = reverse('login')
        self.success_response = self.client.post(url, data)
        self.invalid_response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func.view_class, SignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)

    def test_successful_sign_up(self):
        self.assertRedirects(self.success_response, self.redirected_url)
        self.assertTrue(CustomUser.objects.exists())

    def test_invalid_sign_up(self):
        self.tearDown()
        self.assertEquals(self.invalid_response.status_code, 200)
        form = self.invalid_response.context.get('form')
        self.assertTrue(form.errors)
        self.assertFalse(CustomUser.objects.exists())

    def tearDown(self):
        CustomUser.objects.filter(username='john').delete()


class LoginTests(TestCase):
    def setUp(self):
        data = {
            'username': 'john',
            'email': 'john1991@gmail.com',
            'password': 'abcdef123456',
        }
        self.url = reverse('login')
        self.redirected_url = reverse('home')
        self.response = self.client.get(self.url)
        self.user = CustomUser.objects.create_user(**data)

    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve('/users/login/')
        self.assertEquals(view.func.view_class, LoginView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)

    def test_successful_login(self):
        data = {'username': 'john', 'password': 'abcdef123456'}
        success_response = self.client.post(self.url, data=data)
        self.assertRedirects(success_response, self.redirected_url)

    def test_invalid_login(self):
        invalid_response = self.client.post(self.url, data={})
        self.assertEquals(invalid_response.status_code, 200)
        form = invalid_response.context.get('form')
        self.assertTrue(form.errors)

    def tearDown(self):
        self.user.delete()
