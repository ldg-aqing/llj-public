# presentations/urls.py
from django.urls import path
from .views import speaker_home
from .views import organizer_home
from .views import audience_home
from .views import start_presentation
from . import views


#测试，待规范
from .views import organizer_invite_speaker
from .views import organizer_invite_audience
from .views import organizer_before_presentation



urlpatterns = [
    path('speaker/', speaker_home, name='speaker_home'),
    path('before/<int:presentation_id>/', views.start_presentation, name='speaker_before_presentation'),
    path('organizer/',  organizer_home, name=' organizer_home'),
    path('audience/',  audience_home, name='audience_home'),

    #测试，待规范
    path('organizer_before_prensentation', organizer_before_presentation,name='organizer_before_presentation'),
    path('organizer_invite_audience', organizer_invite_audience,name='organizer_invite_audience'),
    path('organizer_invite_speaker', organizer_invite_speaker,name='organizer_invite_speaker'),
]
