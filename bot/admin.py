from django.contrib import admin

from .models import (
    Client,
    Seller,
    Service,
    Hotel,
    Region
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'tg_id', 'register_at')
    search_fields = ('username', 'tg_id',)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'tg_id', 'register_at')
    search_fields = ('username', 'tg_id',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'region', 'description', 'phone_number', 'price', 'category', 'is_active')
    search_fields = ('name', 'address', 'region', 'phone_number', 'category',)
    list_filter = ('region', 'category')

    @admin.display(description='Диапазон цен')
    def price(self, obj):
        return f'От {obj.min_price}₽ до {obj.max_price}₽'
    price.short_description = 'Диапазон цен'


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'region', 'description', 'phone_number', 'price', 'category', 'is_active')
    search_fields = ('name', 'address', 'region', 'phone_number', 'category',)
    list_filter = ('region', 'category')

    @admin.display(description='Диапазон цен')
    def price(self, obj):
        return f'От {obj.min_price}₽ до {obj.max_price}₽'
    price.short_description = 'Диапазон цен'
    
