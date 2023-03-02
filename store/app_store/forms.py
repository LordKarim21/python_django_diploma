from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('number_card', 'year', 'month')


class PaymentSomeoneForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('number_card', )
