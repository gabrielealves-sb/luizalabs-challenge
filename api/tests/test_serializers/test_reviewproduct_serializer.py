from django.test import TestCase
from faker import Faker
from rest_framework.serializers import ValidationError

from api.models import ReviewProduct, Client, Product
from api.serializers.serializer_reviewproduct import ReviewProductSerializer

fake = Faker()
names = [fake.name() for _ in range(2)]
products = [fake.color() for _ in range(2)]
texts = [fake.text() for _ in range(3)]


class ReviewProductSerializerTestCase(TestCase):
    def setUp(self):
        Client.objects.create(name=names[0], email=fake.email())
        Client.objects.create(name=names[1], email=fake.email())
        Product.objects.create(title=products[0], price=10.00, brand=fake.company())
        ReviewProduct.objects.create(
            author=Client.objects.get(name=names[0]),
            product=Product.objects.get(title=products[0]),
            text=texts[0],
            rate=5
        )

    def test_validate_author_invalid(self):
        """ The validator should raise a ValidationError exception
        when exists a review from the author for the same product """
        old_review = ReviewProduct.objects.get(text=texts[0])
        new_review = ReviewProductSerializer(
            data={
                'author': old_review.author,
                'product': old_review.product,
                'text': texts[1],
                'rate': 5
            }
        )
        self.assertRaises(ValidationError, new_review.validate_author, old_review.author)

    def test_validate_author_valid(self):
        """ The validator should return the value when the author is valid """
        data = {
            'author': Client.objects.get(name=names[1]),
            'product': Product.objects.get(title=products[0]),
            'text': texts[2],
            'rate': 5
        }
        review = ReviewProductSerializer(data=data)
        self.assertEqual(review.validate_author(data['author']), data['author'])
