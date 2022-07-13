from django.test import TestCase
from faker import Faker
from rest_framework.serializers import ValidationError

from api.models import Client, Product, Wishlist
from api.serializers.serializer_wishlist import WishListRequestSerializer

fake = Faker()
clients = [fake.name() for _ in range(4)]
products = [fake.color() for _ in range(2)]


class WishlistSerializerTestCase(TestCase):
    def setUp(self):
        Client.objects.create(name=clients[0], email=fake.email())
        Client.objects.create(name=clients[1], email=fake.email())
        Client.objects.create(name=clients[2], email=fake.email())
        Client.objects.create(name=clients[3], email=fake.email())

        Product.objects.create(title=products[0], price=10.00, brand=fake.company())
        Product.objects.create(title=products[1], price=20.00, brand=fake.company())

        Wishlist.objects.create(client=Client.objects.get(name=clients[1]))
        Wishlist.objects.get(client__name=clients[1]).products.add(Product.objects.get(title=products[0]))
        Wishlist.objects.create(client=Client.objects.get(name=clients[2]))
        Wishlist.objects.create(client=Client.objects.get(name=clients[3]))
        Wishlist.objects.get(client__name=clients[3]).products.add(Product.objects.get(title=products[0]))

    def test_validate_client_valid(self):
        """ The validator should return the initial value when the wishlist client doesn't exist """
        client = Client.objects.get(name=clients[0])
        data = {
            'client': client.id,
        }
        serializer = WishListRequestSerializer(data=data)
        self.assertEqual(serializer.validate_client(data['client']), data['client'])

    def test_validate_client_invalid(self):
        """ The validator should raise a ValidationError exception when exists a wishlist from the client """
        client = Client.objects.get(name=clients[1])
        data = {
            'client': client.id,
        }
        serializer = WishListRequestSerializer(data=data)
        self.assertRaises(ValidationError, serializer.validate_client, client.id)

    def test_validate_products_valid(self):
        """ The validator should return the initial value when the products doesn't exist on wishlist """
        wishlist = Wishlist.objects.get(client__name=clients[2])
        product = Product.objects.get(title=products[0])
        data = {
            'products': [product]
        }
        serializer = WishListRequestSerializer(wishlist, data=data)
        self.assertEqual(serializer.validate_products(data['products']), data['products'])

    def test_validate_products_invalid(self):
        """ The validator should raise a ValidationError exception when exists the product on wishlist """
        wishlist = Wishlist.objects.get(client__name=clients[1])
        product = Product.objects.get(title=products[0])
        data = {
            'products': [product]
        }
        serializer = WishListRequestSerializer(wishlist, data=data)
        self.assertRaises(ValidationError, serializer.validate_products, data['products'])

    def test_validate_remove_products_invalid(self):
        """ The validator should raise a ValidationError when the products doesn't exist on wishlist """
        wishlist = Wishlist.objects.get(client__name=clients[3])
        product = Product.objects.get(title=products[1])
        data = {
            'remove_products': [product]
        }
        serializer = WishListRequestSerializer(wishlist, data=data)
        self.assertRaises(ValidationError, serializer.validate_remove_products, data['remove_products'])

    def test_validate_remove_products_valid(self):
        """ The validator should return the initial value when the products exist on wishlist """
        wishlist = Wishlist.objects.get(client__name=clients[3])
        product = Product.objects.get(title=products[0])
        data = {
            'remove_products': [product]
        }
        serializer = WishListRequestSerializer(wishlist, data=data)
        self.assertEqual(serializer.validate_remove_products(data['remove_products']), data['remove_products'])
