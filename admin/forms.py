# forms.py
from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = uploadImage
        fields = ['image']
