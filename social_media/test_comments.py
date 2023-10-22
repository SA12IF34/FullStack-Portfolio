from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *


# Commenting Tests

class CommentsTestCase(TestCase):

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
        self.client.post("/projects/social_media/posts/", data={
            "content": "hello world",
            "edit_content": "<p>hello world</>"
        }, content_type="application/json")

        self.client.logout()

        self.client.post("/projects/social_media/create-account/", data=data[1], content_type="application/json")


    def test_cearte_comment(self):
        data = {
            "content": "this is stupid"
        }
        res = self.client.post("/projects/social_media/comments/1/", data=data)
        status_code = res.status_code
        self.assertEqual(status_code, 201)

    def test_get_post_comments(self):
        self.test_cearte_comment()

        res = self.client.get("/projects/social_media/comments/1/")
        data = res.json()
        status_code = res.status_code

        self.assertTrue(data[0]['content'] == 'this is stupid')
        self.assertEqual(status_code, 200)

    def test_delete_comment(self):
        self.test_cearte_comment()

        res = self.client.delete("/projects/social_media/comment/1/")
        status_code = res.status_code

        self.assertEqual(status_code, 204)