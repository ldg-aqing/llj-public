# presentations/urls.py
from django.urls import path
from .views import speaker_home
from .views import organizer_home
from .views import audience_home
from . import views
from .views import organizer_during_presentation
from .views import submit_answer_api

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
    path('during/<int:presentation_id>/', organizer_during_presentation, name='organizer_during_presentation'),
    # audience进入演讲页面
    path(
        'audience_during_presentation/<int:presentation_id>/',
        views.audience_during_presentation,
        name='audience_during_presentation'
    ),
    # audience页面AJAX用的API接口
    path(
        'api/presentations/audience_detail/<int:presentation_id>/',
        views.audience_presentation_detail
    ),
    path('api/presentations/submit_answer/', submit_answer_api, name='submit_answer_api'),

    path('after/audience_after/<int:presentation_id>/<int:user_id>/', views.audience_after_view, name='audience_after'),
    path('after/speaker_after/<int:presentation_id>/<int:user_id>/', views.speaker_after_view, name='speaker_after'),
    path('after/organizer_after/<int:presentation_id>/<int:user_id>/', views.organizer_after_view,name='organizer_after'),
]
