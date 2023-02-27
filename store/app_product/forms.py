from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment


class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Comment
        fields = ['name', 'review', 'rate']


class ProductFilterForm(forms.Form):
    is_archived = forms.BooleanField(required=False)
    is_free = forms.BooleanField(required=False)
