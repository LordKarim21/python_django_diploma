from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class ImagePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_image')


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telephone_number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.pk})


class Product(models.Model):
    DELIVERY = [
        ('f', 'free'),
        ('p', 'paid')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    archived = models.BooleanField(default=False)
    delivery = models.CharField(max_length=1, choices=DELIVERY)
    discount = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='product_image')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=36, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(null=True, blank=True)
    review = models.CharField(max_length=200)


class Order(models.Model):
    STATUS_CHOICES = [
        ('p', 'Paid'),
        ('n', 'Not paid')
    ]
    TYPE_DELIVERY = [
        ('s', 'Standard'),
        ('e', 'Express')
    ]
    TYPE_PAYMENT = [
        ('o', 'online'),
        ('s', 'someone')
    ]
    type_delivery = models.CharField(max_length=1, choices=TYPE_DELIVERY)
    type_payment = models.CharField(max_length=1, choices=TYPE_PAYMENT)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    total_cost = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50, null=False, blank=True)
    full_name = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField('OrderItem')
    updated = models.DateField(auto_now=True)

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)


class CartProduct(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, null=True)


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True)
    total_cost = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    def add_product(self, product: 'CartProduct'):
        product = CartProduct.objects.get(id=product.id)
        self.product.add(product)

    def delete_product(self, product: 'CartProduct'):
        product = CartProduct.objects.get(id=product.id)
        self.products.remove(product)


class Payment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    number_card = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_stock(sender, instance, **kwargs):
    id = instance.id
    user = User.objects.get(id=id)
    Profile.objects.update_or_create(id=id, defaults={"user": user})
