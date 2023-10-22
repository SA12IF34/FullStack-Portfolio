from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *


# Notification Tests

class NotificationsTestCase(TestCase):

    def setUp(self):
        data = [
            {
            "username": "saleem",
            "email": "saleem@mail.com", 
            "password": "saleemword",
            "first_name": "saleem", 
            "last_name": "sarhan"
            }, 
            {
            "username": "kareem",
            "email": "kareem@mail.com",
            "password": "kareempswrd",
            "first_name": "kareem",
            "last_name": "akram"
            }
        ]

        self.client.post("/projects/social_media/create-account/", data=data[0], content_type="application/json")
        self.client.logout()

        self.client.post("/projects/social_media/create-account/", data=data[1], content_type="application/json")
        self.client.post("/projects/social_media/follow/", data={"target": 1})
        self.client.logout()

        self.client.post("/projects/social_media/login/", data=data[0], content_type="application/json")

    def test_get_notification(self):
        res = self.client.get("/projects/social_media/notifications/")
        
        data = res.json()
        status_code = res.status_code

        self.assertEqual(status_code, 200)
        self.assertTrue(len(data) > 0)

    def test_delete_notification(self):
        res = self.client.delete("/projects/social_media/notification/1/delete/")
        
        data = res.json()
        status_code = res.status_code

        self.assertEqual(status_code, 205)
        self.assertTrue(len(data) == 0)