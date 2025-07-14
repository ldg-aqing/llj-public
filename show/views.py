from django.shortcuts import render
from .models import Presentation
from users.models import Users  # 你自定义的用户模型
from django.contrib.auth.decorators import login_required

@login_required
def speaker_presentations(request):
    user = request.user
    if user.role != 'SPEAKER':
        return render(request, 'no_permission.html')

    presentations = Presentation.objects.filter(speaker=user)
    return render(request, 'speaker.html', {'presentations': presentations})

@login_required
def organizer_dashboard(request):
    # 示例占位
    return render(request, 'organizer.html')

@login_required
def audience_view(request):
    # 示例占位
    return render(request, 'audience.html')
