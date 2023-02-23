from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Profile, Product, Comment, Order


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, required=False)
    mail = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['telephone_number']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.data.get('mail') or self.data.get('phone'):
            self.instance.user.email = self.data.get('mail')
            self.instance.telephone_number = self.data.get('phone')
        elif self.data.get('password') and self.data.get('passwordReply'):
            if self.data.get('password') == self.data.get('passwordReply') and \
                    self.instance.user.password == self.data.get('passwordCurrent'):
                self.instance.user.set_password(self.data.get('password'))
        self.instance.save()


class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Comment
        fields = ['name', 'review', 'rate']


class ProductFilterForm(forms.Form):
    is_archived = forms.BooleanField(required=False)
    is_free = forms.BooleanField(required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['type_delivery', 'type_payment', 'city', 'address']


class AmountForm(forms.Form):
    amount = forms.IntegerField(required=False)
