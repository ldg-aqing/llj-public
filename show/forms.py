from django import forms
from .models import Presentation

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['title', 'description', 'code', 'start_time', 'end_time']