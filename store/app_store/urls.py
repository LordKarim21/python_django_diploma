from django.urls import path
from .views import *

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('logout', UserLogoutView.as_view(), name='logout'),

    path('', MainView.as_view(), name='main'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/', ProductListView.as_view(), name='products'),

    path('order_create', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
