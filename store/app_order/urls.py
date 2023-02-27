from django.urls import path
from .views import OrderListView, OrderDetailView, OrderCreateView

urlpatterns = [
    path('history-order/', OrderListView.as_view(), name="order_list"),  # TODO получать данные в шаблон
    path('<int:pk>', OrderDetailView.as_view(), name="order_detail"),  # TODO получать данные в шаблон
    path('', OrderCreateView.as_view(), name='order_create'),  # сделать
]