from users.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Presentation
from material.forms import UploadForm
def speaker_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/users/login/')  # 未登录跳转

    # 获取当前登录用户
    try:
        user = User.objects.get(id=user_id, role='SPEAKER')
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': '用户不存在或不是演讲者'})

    # 获取该演讲者的所有演讲
    presentations = Presentation.objects.filter(speaker=user)

    return render(request, 'users/speaker.html', {
        'user': user,
        'presentations': presentations,
    })

def organizer_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/users/login/')  # 未登录跳转

    # 获取当前登录用户
    try:
        user = User.objects.get(id=user_id, role='ORGANIZER')
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': '用户不存在或不是演讲者'})

    # 获取该演讲者的所有演讲
    presentations = Presentation.objects.filter(organizer=user)

    return render(request, 'users/organizer.html', {
        'user': user,
        'presentations': presentations,
    })

def start_presentation(request, pk):
    presentation = get_object_or_404(Presentation, pk=pk)

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.presentation = presentation  # 你可以在模型中添加 presentation 字段
            material.save()
            return redirect('/users/speaker/')  # 上传后跳转
    else:
        form = UploadForm()

    return render(request, "upload.html", {"form": form})


