# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Accounts, uploadAvatarImage


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Accounts
        fields = ('name', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Accounts
        fields = ('name', 'email')


class SignupForm(UserCreationForm):
    email = forms.EmailField(help_text='Required')

    class Meta:
        model = Accounts
        fields = ('name', 'email', 'password1', 'password2')


class AvatarForm(forms.ModelForm):
    class Meta:
        model = uploadAvatarImage
        fields = ['avatar']
