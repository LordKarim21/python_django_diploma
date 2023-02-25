from django.shortcuts import render
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormMixin, FormView
from django.views.generic import DetailView, ListView, UpdateView, View, DeleteView, TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import UserPassesTestMixin


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('account', kwargs={'pk': self.request.user.pk})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"


class UserUpdateView(UpdateView, UserPassesTestMixin):
    model = Profile
    form_class = ProfileForm
    template_name = 'frontend/profile.html'

    def test_func(self):
        user = self.request.user
        return user.has_perm('polls.can_open') or user.has_perm('polls.can_edit')

    def get_success_url(self):
        if self.test_func():
            return reverse_lazy('account_update', kwargs={'pk': self.request.user.pk})


class UserDetailView(DetailView):
    model = Profile
    template_name = 'frontend/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(pk=self.request.user.pk).first()
        return context


class ProductDetailView(DetailView, FormMixin, UserPassesTestMixin):
    model = Product
    form_class = CommentForm
    template_name = 'frontend/product.html'

    def test_func(self):
        user = self.request.user
        return user.has_perm('polls.can_open') or user.has_perm('polls.can_edit')

    def get_success_url(self):
        if self.test_func():
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
    template_name = 'frontend/catalog.html'
    form_class = ProductFilterForm
    paginate_by = 4
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.request.GET)
        if self.request.GET.get('title'):
            title = self.request.GET.get('title')
            queryset = queryset.filter(title=title)
        if self.request.GET.get('available') == 'on':
            queryset = queryset.filter(archived=False)
        if self.request.GET.get('freeDelivery') == 'on':
            queryset = queryset.filter(delivery='f')
        if self.request.GET.get('price'):
            start, end = self.request.GET.get('maxPrice'), self.request.GET.get('minPrice')
            queryset = queryset.filter(price__gte=end, price__lte=start)
        if self.request.GET.get('tag'):
            name = self.request.GET.get('tag')
            queryset = queryset.filter(tag__slug=name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


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


class IndexView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.all()
        context['products'] = queryset.order_by('-comment')
        context['limit_products'] = queryset.filter(quantity__lte=30, quantity__gte=0)
        return context


class SaleView(ListView):
    model = SaleProduct
    template_name = 'frontend/sale.html'
    paginate_by = 20


class PaymentCreateView(CreateView):
    model = Payment
    fields = ['number_card', 'month', 'year']
    template_name = 'frontend/payment.html'

    def get_success_url(self):
        return reverse_lazy('progressPayment', kwargs={'progressPayment': self.request.POST.get('number_card')})


class PaymentSomeoneCreateView(CreateView):
    model = Payment
    fields = ['number_card']
    template_name = 'frontend/paymentsomeone.html'

    def get_success_url(self):
        return reverse_lazy('progressPayment', kwargs={'progressPayment': self.request.POST.get('number_card')})
