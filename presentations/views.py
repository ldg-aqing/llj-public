# presentations/views.py
from django.shortcuts import render

def speaker_before_view(request):
    return render(request, 'presentations/speakerbeforep.html')