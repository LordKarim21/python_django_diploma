from django.contrib import admin
from .models import OrderItem, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['profile', 'city', 'created']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product']


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
