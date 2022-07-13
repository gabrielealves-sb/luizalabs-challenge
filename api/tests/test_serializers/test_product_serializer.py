from django.test import TestCase
from faker import Faker
from rest_framework.serializers import ValidationError

from api.serializers.serializer_product import ProductSerializer

fake = Faker()


class ProductSerializerTestCase(TestCase):
    def test_validate_price_invalid(self):
        """ The validator should raise a ValidationError exception
        when the price is less than 0 """
        data = {
            'title': fake.color(),
            'price': -1,
            'brand': fake.company()
        }
        product = ProductSerializer(data=data)
        self.assertRaises(ValidationError, product.validate_price, data['price'])

    def test_validate_price_valid(self):
        """ The validator should return the value when the price is valid """
        data = {
            'title': fake.color(),
            'price': 10.00,
            'brand': fake.company()
        }
        product = ProductSerializer(data=data)
        self.assertEqual(product.validate_price(data['price']), data['price'])
