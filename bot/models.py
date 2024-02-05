from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserBase(models.Model):
    username = models.CharField(unique=True, db_index=True, verbose_name='Имя пользователя')
    tg_id = models.IntegerField(unique=True, verbose_name='ID Telegram')
    register_at = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        abstract = True

    def __str__(self):
        return self.username


class Client(UserBase):

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Seller(UserBase):

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Category(models.Model):
    name = models.CharField(unique=True)
    type = models.CharField(choices=('Услуги', 'Отели'))

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ServiceBase(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    region = models.CharField(max_length=255, verbose_name='Район')
    description = models.TextField(verbose_name='Описание')
    phone_number = models.CharField(unique=True, max_length=12, verbose_name='Номер телефона')
    max_price = models.PositiveIntegerField(verbose_name='Максимальная цена')
    min_price = models.PositiveIntegerField(verbose_name='Минимальная цена')
    image = ArrayField(models.CharField(), size=3, verbose_name='Фотографии')
    category = models.ForeignKey(Category, related_name='hotels', on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Hotel(ServiceBase):

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class Service(ServiceBase):

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
