from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *


# Likes/Dislikes Tests

class LikesDislikesTestCase(TestCase):

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


    def test_like(self):
        res1 = self.client.get("/projects/social_media/posts/1/")
        post_data = res1.json()
        
        self.assertEqual(post_data['author'], 1)
        
        res2 = self.client.post("/projects/social_media/like/1/")
        post_new_data = res2.json()
        
        self.assertTrue(post_new_data['likes'] == post_data['likes']+1)



    def test_dislike(self):
        res1 = self.client.get("/projects/social_media/posts/1/")
        post_data = res1.json()
        
        self.assertEqual(post_data['author'], 1)
        
        res2 = self.client.post("/projects/social_media/dislike/1/")
        post_new_data = res2.json()
        
        self.assertTrue(post_new_data['dislikes'] == post_data['dislikes']+1)


    def test_unlike(self):
        self.test_like()

        res1 = self.client.get("/projects/social_media/posts/1/")
        post_data = res1.json() 

        self.assertEqual(post_data['author'], 1)

        res2 = self.client.post("/projects/social_media/like/1/")
        post_new_data = res2.json()
        self.assertTrue(post_new_data['likes'] == post_data['likes']-1)

    def test_undislike(self):
        self.test_dislike()
        
        res1 = self.client.get("/projects/social_media/posts/1/")
        post_data = res1.json()

        self.assertEqual(post_data['author'], 1)

        res2 = self.client.post("/projects/social_media/dislike/1/")
        post_new_data = res2.json()
        self.assertTrue(post_new_data['dislikes'] == post_data['dislikes']-1)
