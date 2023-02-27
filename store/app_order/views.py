from .models import *
from app_user.models import Profile
from app_cart.models import CartProduct, Cart
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin


class OrderDetailView(DetailView):
    model = Order
    template_name = 'frontend/oneorder.html'


class OrderListView(ListView):
    model = Order
    template_name = 'frontend/historyorder.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.get(profile=Profile.objects.get(user=self.request.user))
        return queryset


class OrderCreateView(CreateView, UserPassesTestMixin):
    model = Order
    template_name = 'frontend/order.html'
    fields = ['type_delivery', 'type_payment', 'city', 'address']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        cart_product_list = CartProduct.objects.filter(profile=profile)
        context['profile'] = profile
        context['carts'] = cart_product_list
        context['total_cost'] = Cart.objects.get(profile=profile).total_cost
        return context

    def test_func(self):
        user = self.request.user
        return user.has_perm('polls.can_open') or user.has_perm('polls.can_edit')

    def get_success_url(self):
        if self.test_func:
            return reverse_lazy('order_create', kwargs={'pk': self.get_object().id})
        else:
            return reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        context = form.save(commit=False)
        context.product = self.get_object()
        if self.request.user.is_authenticated:
            context.user = self.request.user
            context.username = self.request.user.username
            context.email = self.request.user.email
        context.save()
        return super().form_valid(context)
