from django.test import TestCase
from django.contrib.auth.models import User


class AuthenticationTestCase(TestCase):

    def setUp(self):
        # mock data
        data_1 = { 
            "first_name": "saleem",
            "last_name": "furhan",
            "username": "saleem furhan",
            "email": "saleem@mail.com",
            "password": "saleempswrd"
        }

        data_2 = {
           "first_name": "shareef",
            "last_name": "salmoon",
            "username": "shareef salmoon",
            "email": "shareef@mail.com",
            "password": "shareefpswrd" 
        }

        # creating user
        User.objects.create_user(
            first_name='shareef',
            last_name="salmoon",
            username='shareef shareef',
            email='shareef@mail.com',
            password='shareefpswrd'
        )

        self.data_1 = data_1
        self.data_2 = data_2

    def test_signup_success(self):
        res = self.client.post('/projects/ecommerce/signup/', self.data_1)
        status_code = res.status_code
        self.assertEqual(status_code, 201)

    def test_signup_failur(self):
        res = self.client.post('/projects/ecommerce/signup/', self.data_2)
        status_code = res.status_code
        self.assertEqual(status_code, 306)

    def test_signin_success(self):
        res = self.client.post('/projects/ecommerce/token/', {'username': self.data_2['email'], 'password': self.data_2['password']})
        status_code = res.status_code
        self.assertEqual(status_code, 200)

    def test_signin_failur(self):
        res = self.client.post('/projects/ecommerce/token/', {'username': self.data_1['email'], 'password': self.data_1['password']})
        status_code = res.status_code
        self.assertEqual(status_code, 401)