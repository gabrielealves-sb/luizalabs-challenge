import random

from django.test import TestCase
from faker import Faker
from api.models import Product, Client, ReviewProduct

fake = Faker()
names = [fake.name() for _ in range(2)]
products = [fake.color() for _ in range(2)]
prices = [round(random.uniform(0.00, 1000.00), 2) for _ in range(2)]


class ProductTestCase(TestCase):
    def setUp(self):
        ReviewProduct.objects.create(
            author=Client.objects.create(name=names[0], email=fake.email()),
            product=Product.objects.create(title=products[0], price=prices[0], brand=fake.company()),
            text=fake.text(),
            rate=5
        )
        ReviewProduct.objects.create(
            author=Client.objects.create(name=names[1], email=fake.email()),
            product=Product.objects.get(title=products[0]),
            text=fake.text(),
            rate=2
        )
        Product.objects.create(title=products[1], price=prices[1], brand=fake.company())

    def test_review_score(self):
        """ The review_score property should return the average rate of a product """
        product = Product.objects.get(title=products[0])
        self.assertEqual(product.review_score, 3.5)

    def test_when_review_score_is_empty(self):
        """ The review_score property should return 0 if there are no reviews """
        product = Product.objects.get(title=products[1])
        self.assertEqual(product.review_score, 0)
