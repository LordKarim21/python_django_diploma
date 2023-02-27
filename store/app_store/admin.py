from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'number_card']


admin.site.register(Payment, PaymentAdmin)

