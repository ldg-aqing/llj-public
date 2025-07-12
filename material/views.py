# material/views.py
from django.shortcuts import render
from .models import UploadedMaterial

def material_list(request):
    materials = UploadedMaterial.objects.all()
    return render(request, 'material_list.html', {'materials': materials})
