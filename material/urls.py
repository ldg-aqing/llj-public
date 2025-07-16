from django.urls import path
from . import views

urlpatterns = [
    path('upload/<int:speaker_id>/<int:presentation_id>/', views.upload_material, name='upload_material'),
]
