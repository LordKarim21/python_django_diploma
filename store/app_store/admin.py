from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ['profile']


class CartProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'profile']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'archived']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['profile', 'city', 'created']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'telephone_number', 'image']


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ['image', 'product', ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'review']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'number_card']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['profile']


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)
