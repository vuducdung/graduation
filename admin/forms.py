# forms.py
from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = uploadImage
        fields = ['image']


class MapForm(forms.ModelForm):
    class Meta:
        model = uploadMapImage
        fields = ['map']


class DishForm(forms.ModelForm):
    class Meta:
        model = uploadDishImage
        fields = ['dish']
