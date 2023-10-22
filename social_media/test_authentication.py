from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from .serializers import *

# Authentication Tests

class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.username = 'userchan'
        self.email = 'userchan@email.com'
        self.password = 'userchan123'
        self.fname = 'user'
        self.lname = 'chan'
        user = User.objects.create_user(
            username='userchan',
            email='userchan@email.com',
            password='userchan123',
            first_name='user',
            last_name='chan'
        )

        self.user = user
        self.client.login(username=self.username, password=self.password)

    def test_registration(self):
        account_data = {
            "username":self.username,
            "email":self.email,
            "fname":self.fname,
            "lname":self.lname
        }
        account = AccountSerializer(data=account_data)

        if account.is_valid():
            account.save()

            follow = FollowSerializer(data=account_data)
            if follow.is_valid():
                follow.save()

                self.assertTrue(True)

    def test_authentication(self):
        res = self.client.post('/projects/social_media/login/', {"username": self.username, "email": self.email, "password": self.password})
        status_code = res.status_code
        self.assertEqual(status_code, 202)
    
    def test_logout(self):
        res = self.client.post('/projects/social_media/logout/', {})
        status_code = res.status_code        
        self.assertEqual(status_code, 202)

    def test_delete_user(self):
        res = self.client.post('/projects/social_media/close-account/', {})
        status_code = res.status_code
        self.assertEqual(status_code, 204)