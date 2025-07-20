from users.models import User
from django.shortcuts import render, get_object_or_404, redirect
from presentations.models import Presentation, PresentationAttendee
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

    speakers = User.objects.filter(role='SPEAKER')
    print("Organizer home: SPEAKER count =", speakers.count())

    return render(request, 'users/organizer.html', {
        'presentations': presentations,
        'speakers': speakers  # ✅ 传入模板
    })

def audience_home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/users/login/')  # 未登录跳转

    # 获取当前登录用户对象（必须是听众）
    try:
        user = User.objects.get(id=user_id, role='AUDIENCE')
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': '用户不存在或不是听众'})

    # 获取该听众参与的所有演讲（通过中间表）
    attendee_entries = PresentationAttendee.objects.filter(attendee=user)
    presentations = [entry.presentation for entry in attendee_entries]

    return render(request, 'users/audience.html', {
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

def create_presentation(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/users/login/')

    try:
        organizer = User.objects.get(id=user_id, role='ORGANIZER')
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': '组织者不存在或无权限'})

    speakers = User.objects.filter(role='SPEAKER')  # 一开始就准备好所有 speaker
    print("当前表名：", User._meta.db_table)
    print("SPEAKER 数量：", speakers.count())
    for s in speakers:
        print(s.id, s.username, s.role)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        speaker_id = request.POST.get('speaker_id')

        try:
            speaker = User.objects.get(id=speaker_id, role='SPEAKER')
        except User.DoesNotExist:
            return render(request, 'users/organizer.html', {  # 👈 改成你实际用的模板
                'speakers': speakers,
                'message': '演讲者无效或未选择'
            })

        Presentation.objects.create(
            title=title,
            description=description,
            organizer=organizer,
            speaker=speaker,
            status='PENDING',
        )
        return redirect('/presentations/organizer/')

    # GET 请求也要传入 speakers
    return render(request, 'users/organizer.html', {  # 👈 改成你实际用的模板
        'speakers': speakers
    })

def organizer_before_presentation(request, presentation_id):
    # 先获取该场演讲
    presentation = Presentation.objects.get(id=presentation_id)

    # 获取演讲者与听众信息
    speakers = User.objects.filter(role='SPEAKER')
    audiences = User.objects.filter(role='AUDIENCE')

    return render(request, 'presentations/before/organizer_beforep.html', {
        'presentation': presentation,
        'speakers': speakers,
        'audiences': audiences
    })

#测试，待规范
def organizer_invite_audience(request):
    return render(request, "presentations/before/organizer_invite_audience.html")
def organizer_invite_speaker(request):
    return render(request, "presentations/before/organizer_invite_speaker.html")

def organizer_during_presentation(request):
    return render(request, "presentations/during/organizer_duringp.html")
def audience_during_presentation(request):
    return render(request, "presentations/during/audience_duringp.html")