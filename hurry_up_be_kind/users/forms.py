from django import forms
from django.forms import ClearableFileInput
from .models import FileUser


class FileForm(forms.ModelForm):
    class Meta:
        model = FileUser
        fields = ('file_user', )
        widgets = {
            'file_user': ClearableFileInput(attrs={'multiple': True})
        }