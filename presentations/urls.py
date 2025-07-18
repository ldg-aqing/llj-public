# presentations/urls.py
from django.urls import path
from .views import speaker_home
from .views import organizer_home
from .views import audience_home
from .views import start_presentation
from . import views
from .views import organizer_invite_audience  # 记得引入视图


#测试，待规范
from .views import organizer_invite_speaker
from .views import organizer_invite_audience
from .views import organizer_before_presentation
from .views import organizer_during_presentation
from .views import audience_during_presentation

urlpatterns = [
    path('speaker/', speaker_home, name='speaker_home'),
    path('before/<int:presentation_id>/', views.start_presentation, name='speaker_before_presentation'),
    path('organizer/',  organizer_home, name=' organizer_home'),
    path('audience/',  audience_home, name='audience_home'),
    path('create/', views.create_presentation, name='create_presentation'),

#修改
    path('manage/<int:presentation_id>/', organizer_before_presentation, name='organizer_before_presentation'),


#测试用
    path('organizer_invite_audience', organizer_invite_audience,name='organizer_invite_audience'),
    path('organizer_invite_speaker', organizer_invite_speaker,name='organizer_invite_speaker'),

    path('organizer_during_presentation', organizer_during_presentation, name='organizer_during_presentation'),
    path('audience_during_presentation', audience_during_presentation, name='audience_during_presentation'),

]
