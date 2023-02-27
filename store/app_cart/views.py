from .models import *
from django.urls import reverse_lazy
from django.views.generic import ListView
from app_user.models import Profile


class CartListView(ListView):
    model = CartProduct
    template_name = "frontend/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(profile=Profile.objects.get(user=self.request.user))
        if cart:
            context['total_cost'] = cart.total_cost
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('product'):
            cart_product_id = self.request.GET.get('product')
            cart_product = queryset.filter(product__product__pk=cart_product_id).first()
            cart_product.delete()
        return queryset
