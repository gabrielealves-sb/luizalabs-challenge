from statistics import mean, StatisticsError
from django.db import models


RATE_CHOICES = (
    (1, '1 Star'),
    (2, '2 Stars'),
    (3, '3 Stars'),
    (4, '4 Stars'),
    (5, '5 Stars'),
)


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, blank=True, null=True)
    brand = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    @property
    def review_score(self):
        try:
            reviews = ReviewProduct.objects.filter(product=self)
            return mean(reviews.values_list('rate', flat=True))
        except StatisticsError:
            return 0

    def __str__(self):
        return self.title


class ReviewProduct(models.Model):
    author = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(max_length=140, blank=True)
    rate = models.IntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return self.product.title


class Wishlist(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.client.name
