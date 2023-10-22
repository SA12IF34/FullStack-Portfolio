from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *

# Searching Tests

class SearchTestCase(TestCase):

    def setUp(self):
        data = [
            {
            "user": 1,
            "username":'saleem',
            "email":'user1@mail.com',
            "fname":'user',
            "lname":'chan'
            },
            {
            "user": 2,
            "username":'kareem',
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

    def test_search(self):
        res1 = self.client.get(f'/projects/social_media/search/ka/')
        res2 = self.client.get(f'/projects/social_media/search/sa/')
        status_code1 = res1.status_code
        status_code2 = res2.status_code
        self.assertEqual(status_code1, 200)
        self.assertEqual(status_code2, 200)