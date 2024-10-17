from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Category, Brand


class ProductCRUDTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='TestCategory')
        self.brand = Brand.objects.create(name='TestBrand')
        self.product = Product.objects.create(
            name='TestProduct',
            description='TestDescription',
            price=10.99,
            stock=100,
            category=self.category,
            brand=self.brand,
        )

    def test_product_create(self):
        response = self.client.post(reverse('product_create'), {
            'name': 'NewProduct',
            'description': 'NewDescription',
            'price': 15.99,
            'stock': 50,
            'category': self.category.id,
            'brand': self.brand.id,
        })
        self.assertEqual(response.status_code, 302)
        product_exists = Product.objects.filter(name='NewProduct').exists()
        self.assertTrue(product_exists)

    def test_product_update(self):
        response = self.client.post(reverse('product_update', args=[self.product.pk]), {
            'name': 'UpdatedProduct',
            'description': 'UpdatedDescription',
            'price': 20.99,
            'stock': 200,
            'category': self.category.id,
            'brand': self.brand.id,
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'UpdatedProduct')
        self.assertEqual(self.product.description, 'UpdatedDescription')
        self.assertEqual(float(self.product.price), 20.99)
        self.assertEqual(self.product.stock, 200)

    def test_product_delete(self):
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        product_exists = Product.objects.filter(name='TestProduct').exists()
        self.assertFalse(product_exists)
