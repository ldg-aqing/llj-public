# material/forms.py
from django import forms
from .models import UploadedMaterial

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedMaterial
        fields = ['title', 'file', 'file_type']
