from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.
class ApiUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Клиент'),
        ('seller', 'Поставщик')
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES)


class Store(models.Model):
    name = models.CharField(max_length=128)
    address = models.TextField()

    def __str__(self):
        return f'Склад {self.id}: {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, related_name = 'products',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f'Товар {self.id}: {self.name}. Цена: {self.price} '


class Order(models.Model):
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}; {self.product.name}; {self.product.store.name}'