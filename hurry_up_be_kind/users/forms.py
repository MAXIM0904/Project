from django import forms
from django.forms import ClearableFileInput
from .models import AvatarUser


class ImgForm(forms.ModelForm):
    class Meta:
        model = AvatarUser
        fields = ('avatar_user_img', )
        widgets = {
            'avatar_user_img': ClearableFileInput(attrs={'multiple': True})
        }