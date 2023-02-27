from django.db import models
from app_user.models import Profile
from app_product.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('p', 'paid'),
        ('n', 'not paid')
    ]
    TYPE_DELIVERY = [
        ('o', 'ordinary'),
        ('e', 'express')
    ]
    TYPE_PAYMENT = [
        ('o', 'online'),
        ('s', 'someone')
    ]
    type_delivery = models.CharField(max_length=1, choices=TYPE_DELIVERY)
    type_payment = models.CharField(max_length=1, choices=TYPE_PAYMENT)
    total_cost = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    updated = models.DateField(auto_now=True)

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
