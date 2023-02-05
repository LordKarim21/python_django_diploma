from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    archived = models.BooleanField(default=False)


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=36, blank=True, null=True)
    text = models.CharField(max_length=200)


class Order(models.Model):
    STATUS_CHOICES = [
        ('d', 'Delivered at'),
        ('p', 'Paid'),
        ('n', 'Not paid')
    ]
    type = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)
    total_cost = models.PositiveIntegerField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telephone_number = models.ImageField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)


@receiver(post_save, sender=User)
def update_stock(sender, instance, **kwargs):
    id = instance.id
    user = User.objects.get(id=id)
    Profile.objects.update_or_create(id=id, defaults={"user": user})
