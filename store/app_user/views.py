from .models import *
from .forms import *
from app_order.models import Order
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
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
