from django.contrib import admin
from .models import Cart, CartProduct


class CartAdmin(admin.ModelAdmin):
    list_display = ['profile']


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'profile']


admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
