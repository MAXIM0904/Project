from django import forms
from django.forms import ClearableFileInput
from .models import AvatarUser


class ImgForm(forms.ModelForm):
    class Meta:
        model = AvatarUser
        fields = ('file_user', )
        widgets = {
            'file_user': ClearableFileInput(attrs={'multiple': True})
        }