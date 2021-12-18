from django.test import TestCase
from django.test.client import Client
from mainapp.models import ProducCategory, Product


class TestMainappSmoke(TestCase):
    status_ok = 200
    status_redirect = 302

    def setUp(self) -> None:
        self.category = ProducCategory.objects.create(
            name='cat1'
        )
        for i in range(10):
            Product.objects.create(
                name=f'prod1 {i}',
                category=self.category,
                short_desc='shortdesc',
                description='desc'
            )

        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, self.status_ok)

    def test_products_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.status_ok)

    def test_categories_urls(self):
        for cat in ProducCategory.objects.all():
            response = self.client.get(f'/products/category/{cat.pk}/')
            self.assertEqual(response.status_code, self.status_ok)





