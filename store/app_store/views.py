from django.shortcuts import render
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormMixin, FormView
from django.views.generic import DetailView, ListView, UpdateView, View
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateProfile


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


class MainView(View):
    def get(self, request):
        return render(request, 'users/main.html')


class IndexView(View):
    def get(self, request):
        return render(request, 'django-frontend/index.html')

