from .models import *
from .forms import *
from app_cart.models import Cart, CartProduct
from app_user.models import Profile
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin


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
        product = self.get_object()
        review = form.cleaned_data['review']
        rate = form.cleaned_data['rate']
        name = form.cleaned_data['name']
        comment = Comment()
        comment.create(product=product, review=review, rate=rate, name=name)
        return super().form_valid(context)


class ProductListView(ListView, FormMixin):
    template_name = 'frontend/catalog.html'
    form_class = ProductFilterForm
    paginate_by = 4
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
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


class SaleView(ListView):
    model = SaleProduct
    template_name = 'frontend/sale.html'
    paginate_by = 20
