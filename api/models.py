from datetime import datetime

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
    address = models.TextField(blank=True)
    user = models.ForeignKey(ApiUser, related_name='stores',
                             on_delete=models.PROTECT)

    def __str__(self):
        return f'Склад {self.id}: {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    user = models.ForeignKey(ApiUser, related_name='products',
                             on_delete=models.PROTECT)

    def __str__(self):
        return (f'Товар {self.id}: {self.name}. Цена: {self.price}.')


class Supply(models.Model):
    product = models.ForeignKey(Product, related_name='supplies',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    store = models.ForeignKey(Store, related_name='supplies',
                              on_delete=models.CASCADE,)
    user = models.ForeignKey(ApiUser, related_name='supplies',
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Поставка: {self.id}. \n'
                f'Товар: {self.product.name}. \n'
                f'Склад: {self.store.name}. \n'
                f'Поставщик:{self.user.username}. \n'                
                f'Количество {self.quantity}')


class Order(models.Model):
    product = models.ForeignKey(Product, related_name='orders',
                                on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='orders',
                              on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(ApiUser, related_name='orders',
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Заказ: {self.id}.\n'
                f'Товар {self.product.id}: {self.product.name}.\n'
                f'Количество: {self.quantity}.\n'                
                f'Склад {self.store.id}: {self.store.name}.\n'                
                f'Покупатель {self.user.id}: {self.user.username}.'
                f'Дата заказа: {self.date}')


# class Availability(models.Model):
#     store = models.ForeignKey(Store, related_name='availability',
#                               on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='availability',
#                                 on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
#     def __str__(self):
#         return(f'Доступность на складе.\n'
#                f'Товар {self.product.id}: {self.product.name}.\n'
#                f'Склад {self.store.id}: {self.store.name}.\n'
#                f'Количество: {self.quantity}')
