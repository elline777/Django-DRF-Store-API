from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class ApiUser(AbstractUser):
    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('customer', 'Customer'),
        ('seller', 'Seller')
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)


class Store(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField()


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, related_name = 'products',
                              on_delete=models.CASCADE)


class Order(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, related_name='orders', on_delete=models.CASCADE)