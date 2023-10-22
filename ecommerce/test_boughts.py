from django.test import TestCase
from django.contrib.auth.models import User

class BoughtsTestCase(TestCase):

    def setUp(self):
        data = {
            'first_name': 'saif',
            'last_name': 'chan',
            'username': 'saifchan',
            'email': 'saifchan@mail.com',
            'password': 'saifsaif'
        }
        res = self.client.post('/projects/ecommerce/signup/', data, content_type='application/json')
        creds = res.json()
        self.headers = {
            "HTTP_AUTHORIZATION": f"Bearer {creds['access']}"
        } 

    def test_add_to_boughts(self):
        res = self.client.post('/projects/ecommerce/boughts/', data={
            'product_name': 'my perfume',
            'image': 'https://fimgs.net/mdimg/perfume/375x500.53.jpg'
        }, **self.headers)
        status_code = res.status_code
        self.assertEqual(status_code, 201)

    def test_get_boughts(self):
        self.test_add_to_boughts()

        res = self.client.get('/projects/ecommerce/boughts/', **self.headers)
        status_code = res.status_code
        self.assertEqual(status_code, 200)
        self.assertTrue(len(res.json()) == 1)
