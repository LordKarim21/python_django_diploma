from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('<int:pk>/', UserDetailView.as_view(), name='account'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/', ProductListView.as_view(), name='products'),

    path('order_create', OrderCreateView.as_view(), name='order_create'),
    path('history', OrderListView.as_view(), name='history'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

    path('cart_list', CartListView.as_view(), name='cart_list'),
]
