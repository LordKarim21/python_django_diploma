from django.urls import path
from .views import ProductListView, ProductDetailView, SaleView

urlpatterns = [
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('sale/', SaleView.as_view(), name='sale'),
]
