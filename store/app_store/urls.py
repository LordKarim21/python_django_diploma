from django.urls import path
from django.views.generic import TemplateView
from .views import IndexView, PaymentCreateView, PaymentSomeoneCreateView

urlpatterns = [
    path('', IndexView.as_view(), name="home"),
    path('about/', TemplateView.as_view(template_name="frontend/about.html"), name="about"),


    path('payment/', PaymentCreateView.as_view(), name="payment"),  # TODO реализовать отправку формы оплаты
    path('payment-someone/', PaymentSomeoneCreateView.as_view(), name="paymentsomeone"),  # TODO реализовать отправку формы оплаты

    path('progress-payment/', TemplateView.as_view(template_name="frontend/progressPayment.html"), name='progressPayment'),
]
