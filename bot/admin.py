from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

import requests

from .models import (
    Client,
    Seller,
    Service,
    Hotel,
    Region,
    Category
)

from bot.forms import SendMessageForm
from constants import TOKEN


@admin.action(description='Разослать сообщения')
def send_messages(modeladmin, request, queryset):
    form = None

    if 'apply' in request.POST:
        form = SendMessageForm(request.POST)

        if form.is_valid():
            count = 0
            text = form.cleaned_data['text']
            for user in queryset:
                tg_id = user.tg_id
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={tg_id}&text={text}"
                requests.get(url)
                count += 1

            modeladmin.message_user(request, f'Было отправлено {count} сообщений.', level='success')
            return HttpResponseRedirect(request.get_full_path())
    if not form:
        form = SendMessageForm(initial={'_selected_action': queryset.values_list('id', flat=True)})

    return render(request, 'bot/send_messages.html', {'form': form, 'items': queryset})


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'tg_id', 'register_at')
    search_fields = ('username', 'tg_id',)
    actions = [send_messages]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'tg_id', 'register_at')
    search_fields = ('username', 'tg_id',)
    actions = [send_messages]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'region', 'description', 'phone_number', 'price', 'category', 'is_active')
    search_fields = ('name', 'address', 'region', 'phone_number', 'category',)
    list_filter = ('region', 'category')

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.base_fields['category'].queryset = Category.objects.filter(type='Услуги')
        return form

    @admin.display(description='Диапазон цен')
    def price(self, obj):
        return f'От {obj.min_price}₽ до {obj.max_price}₽'
    price.short_description = 'Диапазон цен'


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'region', 'description', 'phone_number', 'price', 'category', 'is_active')
    search_fields = ('name', 'address', 'region', 'phone_number', 'category',)
    list_filter = ('region', 'category')

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.base_fields['category'].queryset = Category.objects.filter(type='Отели')
        return form

    @admin.display(description='Диапазон цен')
    def price(self, obj):
        return f'От {obj.min_price}₽ до {obj.max_price}₽'
    price.short_description = 'Диапазон цен'
    
