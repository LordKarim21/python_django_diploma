from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path('about/', TemplateView.as_view(template_name="frontend/about.html"), name="about"),
    path('account/<int:pk>', UserDetailView.as_view(), name="account"),  # TODO получать данные в шаблон

    path('cart/', CartListView.as_view(), name='cart'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    # path('catalog/<int:pk>', TemplateView.as_view(template_name="frontend/catalog.html"), name='catalog_detail'),

    path('history-order/', OrderListView.as_view(), name="order_list"),  # TODO получать данные в шаблон
    path('order-detail/<int:pk>', OrderDetailView.as_view(), name="order_detail"),  # TODO получать данные в шаблон
    path('order/', OrderCreateView.as_view(), name='order_create'),  # сделать

    path('payment/', TemplateView.as_view(template_name="frontend/payment.html"), name="payment"),  # TODO реализовать отправку формы оплаты
    path('payment-someone/', TemplateView.as_view(template_name="frontend/paymentsomeone.html"), name="paymentsomeone"),  # TODO реализовать отправку формы оплаты

    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),

    path('profile/<int:pk>', UserUpdateView.as_view(), name="account_update"),  # TODO получать данные в шаблон
    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html"), name='progressPayment'),
    path('sale/', SaleView.as_view(), name='sale'),
]
