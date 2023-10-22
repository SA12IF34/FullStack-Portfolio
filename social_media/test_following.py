from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *


# Following Tests

class FollowTestCase(TestCase):

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

            data[0].pop('email')
            data[1].pop('email')
            data[0]['name'] = data[0]['username']
            data[1]['name'] = data[1]['username']
            data[0].pop('username')
            data[1].pop('username')

            follow1 = FollowSerializer(data=data[0])
            follow2 = FollowSerializer(data=data[1])
            
            if follow1.is_valid() and follow2.is_valid():
                follow1.save()
                follow2.save()
                
                self.account1 = account1.data
                self.account2 = account2.data

                self.follow1 = follow1.data
                self.follow2 = follow2.data

            self.client.login(username="userchan", password="userchan123")

    def test_follow(self):
        res = self.client.post('/projects/social_media/follow/', {"target": 2})
        status_code = res.status_code
        self.assertEqual(status_code, 202)



    def test_unfollow(self):
        self.test_follow()

        res = self.client.post('/projects/social_media/unfollow/', {"target": 2})
        status_code = res.status_code
        self.assertEqual(status_code, 202)

    def test_get_followers(self):
        self.test_follow()

        res = self.client.get('/projects/social_media/accounts/2/')
        status_code = res.status_code
        data = res.json()
        self.assertTrue('followers' in data.keys())
        self.assertTrue(len(data['followers']) > 0)
        self.assertEqual(status_code, 200)

    def test_get_followings(self):
        self.test_follow()

        res = self.client.get('/projects/social_media/follow/')
        status_code = res.status_code
        data = res.json()
        self.assertEqual(status_code, 200)
        self.assertTrue(self.account2['username'] in data[0]['username'])