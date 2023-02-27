from .models import Payment
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


class IndexView(TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.all()
        context['products'] = queryset.order_by('-comment')
        context['limit_products'] = queryset.filter(quantity__lte=30, quantity__gte=0)
        return context


class PaymentCreateView(CreateView):
    model = Payment
    fields = ['number_card', 'month', 'year']
    template_name = 'frontend/payment.html'

    def get_success_url(self):
        return reverse_lazy('progressPayment', kwargs={'progressPayment': self.request.POST.get('number_card')})


class PaymentSomeoneCreateView(CreateView):
    model = Payment
    fields = ['number_card']
    template_name = 'frontend/paymentsomeone.html'

    def get_success_url(self):
        return reverse_lazy('progressPayment', kwargs={'progressPayment': self.request.POST.get('number_card')})
