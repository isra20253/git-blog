from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SignUpTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='existing', password='p')

    def test_signup_duplicate_username_shows_error(self):
        resp = self.client.post(reverse('users-sign_up'), {
            'username': 'existing',
            'email': 'x@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        # Should not redirect; should re-render form with error
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ce nom d\'utilisateur est déjà utilisé')
from django.test import TestCase

# Create your tests here.
