from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, Profile


class CreateProfile(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False)
    telephone_number = forms.IntegerField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('password1', 'password2',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('username', 'text', )


class UpdateProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['telephone_number', 'image']

