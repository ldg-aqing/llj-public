# presentations/urls.py
from django.urls import path
from .views import speaker_home
from .views import organizer_home
from .views import audience_home
from . import views
from .views import organizer_invite_speaker
from .views import organizer_invite_audience
from .views import organizer_during_presentation
from .views import audience_during_presentation

urlpatterns = [
    path('speaker/', speaker_home, name='speaker_home'),
    path('before/<int:presentation_id>/', views.start_presentation, name='speaker_before_presentation'),
    path('organizer/',  organizer_home, name=' organizer_home'),
    path('audience/',  audience_home, name='audience_home'),
    path('create/', views.create_presentation, name='create_presentation'),

#修改
    path('manage/<int:presentation_id>/', views.manage_presentation, name='manage_presentation'),
    path('organizer_invite_speaker/<int:presentation_id>/', views.organizer_invite_speaker, name='organizer_invite_speaker'),
    path('organizer_invite_audience/<int:presentation_id>/', views.organizer_invite_audience, name='organizer_invite_audience'),
    path('invite_audience/', views.invite_audience, name='invite_audience'),
    path('remove_audience/', views.remove_audience, name='remove_audience'),
    path('preview_file/<int:file_id>/', views.preview_file, name='preview_file'),
    path('start/<int:presentation_id>/', views.start_presentation, name='start_presentation'),

#测试用

    path('during/<int:presentation_id>/', views.organizer_during_presentation, name='organizer_during_presentation'),
    path('audience_during_presentation', audience_during_presentation, name='audience_during_presentation'),

]
