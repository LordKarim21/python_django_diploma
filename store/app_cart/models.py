from django.db import models
from app_product.models import Product
from app_user.models import Profile


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=True, null=True)

    def add_product(self, product: Product, profile: Profile, quantity: int):
        cart = Cart.objects.get(profile=profile)
        CartProduct.objects.update_or_create(cart=cart, product=product, profile=profile, quantity=quantity)

    def delete_product(self, product: Product):
        cart_item = CartProduct.objects.get(product=product)
        cart_item.delete()

    def update_quantity(self, quantity: int, product: Product):
        cart_item = CartProduct.objects.get(product=product)
        cart_item.quantity = quantity
        cart_item.save()

    def get_cart_items(self, profile: Profile):
        return CartProduct.objects.filter(profile=profile)

    def get_count_cart_items(self, profile: Profile):
        return CartProduct.objects.filter(profile=profile).count()


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total_cost = models.DecimalField(decimal_places=1, max_digits=100, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
