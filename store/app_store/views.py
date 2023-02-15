from django.shortcuts import render
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormMixin, FormView
from django.views.generic import DetailView, ListView, UpdateView, View, DeleteView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('account', kwargs={'pk': self.request.user.pk})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('products')


class UserUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'django-frontend/profile.html'

    def get_success_url(self):
        return reverse_lazy('account', kwargs={'pk': self.request.user.pk})


class UserDetailView(DetailView):
    model = Profile
    template_name = 'django-frontend/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(pk=self.request.user.pk).first()
        return context


class ProductDetailView(DetailView, FormMixin, UserPassesTestMixin):
    model = Product
    form_class = CommentForm
    template_name = 'django-frontend/product.html'

    def test_func(self):
        user = self.request.user
        return user.has_perm('polls.can_open') or user.has_perm('polls.can_edit')

    def get_success_url(self):
        if self.test_func:
            return reverse_lazy('product_detail', kwargs={'pk': self.get_object().id})
        else:
            return reverse_lazy('login')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('amount'):
            product = Product.objects.get(id=self.kwargs.get('pk'))
            quantity = self.request.GET.get('amount')
            profile = Profile.objects.get(user=self.request.user)
            if not CartProduct.objects.filter(product=product):
                cart_product = CartProduct.objects.create(profile=profile, quantity=quantity, product=product)

            else:
                cart_product = CartProduct.objects.get(product=product)
                cart_product.quantity = quantity
                cart_product.save()
            total_cost = int(product.price) * int(quantity)
            if not Cart.objects.filter(product=cart_product):
                cart = Cart.objects.create(profile=profile, total_cost=float(total_cost))
                cart.add_product(cart_product)
            else:
                cart = Cart.objects.get(product=cart_product)
                cart.total_cost = total_cost
        return queryset

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if 'email' not in form.fields and 'username' not in form.fields:
            form.fields['email'] = request.user.email if request.user.email else 'anonim@anonim.ok'
            form.fields['username'] = request.user.username if request.user.username else 'anonim'
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


class ProductListView(ListView, FormMixin):
    template_name = 'django-frontend/catalog.html'
    form_class = ProductFilterForm
    paginate_by = 4
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('title'):
            title = self.request.GET.get('title')
            queryset = queryset.filter(title=title)
        if self.request.GET.get('is_archived'):
            queryset = queryset.filter(archived=False)
        if self.request.GET.get('is_free'):
            queryset = queryset.filter(delivery='f')
        if self.request.GET.get('created'):
            queryset = queryset.order_by('-created')
        if self.request.GET.get('sort_price'):
            queryset = queryset.order_by('price')
        if self.request.GET.get('price'):
            start, end = self.request.GET.get('price').split(';')
            queryset = queryset.filter(price__gte=start, price__lte=end)
        if self.request.GET.get('tag'):
            tag = self.request.GET.get('tag')
            queryset = queryset.filter(tag__name=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class OrderDetailView(DetailView):
    model = Order
    template_name = 'django-frontend/oneorder.html'


class OrderListView(ListView):
    model = Order
    template_name = 'django-frontend/historyorder.html'


class OrderCreateView(CreateView):
    model = Order
    template_name = 'django-frontend/order.html'
    fields = ['type_delivery', 'type_payment', 'city', 'address']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('product'):
            self.product = self.request.GET.get('product')
        return context

    def get_success_url(self):
        return reverse_lazy('order_detail', kwargs={'pk': self.get_object().id})

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


class CartListView(ListView):
    model = Cart
    template_name = "django-frontend/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_cost'] = sum(int(item.total_cost) for item in self.object_list)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('product'):
            cart_product_id = self.request.GET.get('product')
            cart_product = queryset.filter(product__product__pk=cart_product_id).first()
            cart_product.delete()
        return queryset
