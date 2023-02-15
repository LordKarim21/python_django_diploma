from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Profile, Product, Comment, Order


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['telephone_number', 'image']


class ProductForm(forms.ModelForm):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Product
        fields = ['title', 'description', 'price']


class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Comment
        fields = ['username', 'text']


class ProductFilterForm(forms.Form):
    is_archived = forms.BooleanField(required=False)
    is_free = forms.BooleanField(required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['type_delivery', 'type_payment', 'city', 'address']


class AmountForm(forms.Form):
    amount = forms.IntegerField(required=False)
