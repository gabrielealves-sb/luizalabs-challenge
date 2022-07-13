from django.test import TestCase
from faker import Faker
from rest_framework.serializers import ValidationError

from api.serializers.serializer_user import UserSerializer

fake = Faker()


class UserSerializerTestCase(TestCase):
    def test_create_new_user(self):
        """ Should save the user to the database and return a User object """
        data = {"username": fake.email(), "password": fake.password()}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), True)
