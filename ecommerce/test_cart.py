from django.test import TestCase
from django.contrib.auth.models import User

class CartTestCase(TestCase):

    def setUp(self):
        self.data = {
            "username": 'saif@mail.com',
            "password": 'saifsaif'
        }

        User.objects.create_user(
            username='saif',
            first_name='saif',
            last_name='saleem',
            email='saif@mail.com',
            password='saifsaif'
        )

        res = self.client.post('/projects/ecommerce/token/', self.data, content_type='application/json')
        self.creds = res.json()

        self.headers = {
            "HTTP_AUTHORIZATION": f"Bearer {self.creds['access']}"
        }

    def test_cart_get_success(self):
        res = self.client.get('/projects/ecommerce/cart/', **self.headers)
        status_code = res.status_code
        self.assertEqual(status_code, 200)

    def test_cart_get_failur(self):
        res = self.client.get('/projects/ecommerce/cart/')
        status_code = res.status_code
        self.assertEqual(status_code, 401)

    def test_add_to_cart(self):
        res = self.client.post('/projects/ecommerce/cart/', {
            'product_name': 'my perfume',
            'price': 15,
            'image': 'https://fimgs.net/mdimg/perfume/375x500.53.jpg'
        }, **self.headers)

        status_code = res.status_code
        self.assertEqual(status_code, 201)
    
    def test_delete_from_cart(self):
        self.test_add_to_cart()
        
        name = 'my perfume'
        res = self.client.delete(f'/projects/ecommerce/cart/{name}/delete/', **self.headers)
        status_code = res.status_code
        self.assertEqual(status_code, 204)
