from django import forms
from django.forms import ClearableFileInput
from .models import ImgFileConfectionary


class ImgConfectionaryForm(forms.ModelForm):
    class Meta:
        model = ImgFileConfectionary
        fields = ('img_confectionary', )
        widgets = {
            'img_confectionary': ClearableFileInput(attrs={'multiple': True})
        }