from django.shortcuts import render
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormMixin, FormView
from django.views.generic import DetailView, ListView, UpdateView, View
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateProfile
from django.core.paginator import Paginator


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('main')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')


class UserRegisterView(CreateView):
    form_class = CreateProfile
    template_name = 'django-frontend/profile.html'
    success_url = reverse_lazy('main')


class UserDetailView(DetailView):
    model = Profile
    template_name = 'django-frontend/account.html'


class MainView(View):
    def get(self, request):
        return render(request, 'users/main.html')


class ProductDetailView(DetailView, FormMixin):
    model = Product
    form_class = CommentForm
    template_name = 'django-frontend/product.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.get_object().id,})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['images'] = Image.objects.filter(product=product)
        context['comments'] = Comment.objects.filter(product=product)
        return context

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
        return queryset


class OrderDetailView(DetailView):
    model = Order
    template_name = 'django-frontend/oneorder.html'


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
        return reverse_lazy('order_detail', kwargs={'pk': self.get_object().id,})

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
