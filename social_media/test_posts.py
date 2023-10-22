from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *



# Posting Tests

class PostsTestCase(TestCase):

    def setUp(self):
        data = {
            "username": "saleem",
            "email": "saleem@mail.com", 
            "password": "saleemword",
            "first_name": "saleem", 
            "last_name": "sarhan"
        }

        self.client.post("/projects/social_media/create-account/", data=data, content_type="application/json")

    def test_create_post(self):
        data = {
            "content": "hello world",
            "edit_content": "<p>hello world</p>"
        }

        res = self.client.post("/projects/social_media/posts/", data=data, content_type="application/json")
        status_code = res.status_code
        self.assertEqual(status_code, 201)

    def test_get_post(self):
        self.test_create_post()

        res = self.client.get("/projects/social_media/posts/1/")
        status_code = res.status_code
        self.assertEqual(status_code, 200)

    def test_edit_post_succeed(self):
        self.test_create_post()        

        data = {
            "content": "new content",
            "edit_content": "<h2>new content</h2>"
        }
        res = self.client.patch("/projects/social_media/posts/1/edit/", data=data, content_type="application/json")
        status_code = res.status_code
        self.assertEqual(status_code, 202)

    def test_delete_post(self):
        self.test_create_post()

        res = self.client.delete("/projects/social_media/posts/1/")
        status_code = res.status_code
        self.assertEqual(status_code, 202)