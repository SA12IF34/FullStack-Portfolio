from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import login
from .serializers import *


# Accounts Tests

class AccountsTestCase(TestCase):

    def setUp(self):
        data = [
            {
            "user": 1,
            "username":'userchan',
            "email":'user1@mail.com',
            "fname":'user',
            "lname":'chan'
            },
            {
            "user": 2,
            "username":'chanuser',
            "email":'user2@mail.com',
            "fname":'chan',
            "lname":'user'
            }
        ]
        user1 = User.objects.create_user(
            username=data[0]['username'],
            email=data[0]['email'],
            password='userchan123',
            first_name=data[0]['fname'],
            last_name=data[0]['lname']
        )
        user2 = User.objects.create_user(
            username=data[1]['username'],
            email=data[1]['email'],
            password='userchan321',
            first_name=data[1]['fname'],
            last_name=data[1]['lname']
        )

        
        self.user1 = user1
        self.user2 = user2
        
        account1 = AccountSerializer(data=data[0])
        account2 = AccountSerializer(data=data[1])

        if account1.is_valid() and account2.is_valid():
            account1.save()
            account2.save()
            self.client.login(username="userchan", password="userchan123")

    def test_get_Accounts(self):
        res = self.client.get('/projects/social_media/accounts/')
        status_code = res.status_code
        self.assertEqual(status_code, 200)

    def test_get_user_account(self):
        res = self.client.get('/projects/social_media/me/')
        status_code = res.status_code
        self.assertEqual(status_code, 200)

    def test_get_account(self):
        res = self.client.get(f'/projects/social_media/accounts/{1}/')
        status_code = res.status_code
        self.assertEqual(status_code, 200)

    def test_change_username(self):
        res = self.client.patch(f'/projects/social_media/me/', {"username": "userchan001"}, 'application/json')
        status_code = res.status_code
        self.assertEqual(status_code, 202)

    def test_change_email(self):
        res = self.client.patch('/projects/social_media/me/', {"email": "userchan@mail.com"}, 'application/json')
        status_code = res.status_code
        self.assertEqual(status_code, 202)

    def test_change_password(self):
        res = self.client.patch('/projects/social_media/me/', {"password": "newpassword001"}, 'application/json')
        status_code = res.status_code
        self.assertEqual(status_code, 202)

    def test_fails_with_400(self):
        res = self.client.patch('/projects/social_media/me/', content_type='application/json')
        status_code = res.status_code
        self.assertEqual(status_code, 400)