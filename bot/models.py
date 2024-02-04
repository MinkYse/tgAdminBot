from django.db import models
from django.contrib.postgres.fields import ArrayField


class Client(models.Model):
    username = models.CharField(unique=True, db_index=True)
    tg_id = models.IntegerField(unique=True)
    register_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.username


class Seller(models.Model):
    username = models.CharField(unique=True, db_index=True)
    tg_id = models.IntegerField(unique=True)
    register_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(unique=True)
    type = models.CharField(choices=('Услуги', 'Отели'))


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    phone_number = models.CharField(unique=True, max_length=12)
    max_price = models.PositiveIntegerField()
    min_price = models.PositiveIntegerField()
    image = ArrayField(models.CharField(), size=3)
    category = models.ForeignKey(Category, related_name='hotels', on_delete=models.CASCADE)


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    phone_number = models.CharField(unique=True, max_length=12)
    max_price = models.PositiveIntegerField()
    min_price = models.PositiveIntegerField()
    image = ArrayField(models.CharField(), size=3)
    category = models.ForeignKey(Category, related_name='hotels', on_delete=models.CASCADE)