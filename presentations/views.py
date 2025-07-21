from users.models import User
from django.shortcuts import render, get_object_or_404, redirect
from presentations.models import Presentation, PresentationAttendee
from material.forms import UploadForm
from uploads.models import Upload
from django.views.decorators.http import require_POST
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

    return render(request, 'users/organizer.html', {
        'user': user,
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
def manage_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    organizer = presentation.organizer
    speaker = presentation.speaker
    attendee_objs = PresentationAttendee.objects.filter(presentation=presentation)
    attendees = [a.attendee for a in attendee_objs if a.attendee != speaker]

    uploads = Upload.objects.filter(presentation=presentation)

    context = {
        'presentation': presentation,
        'organizer': organizer,
        'speaker': speaker,
        'attendees': attendees,
        'uploads': uploads,
    }
    return render(request, 'presentations/before/organizer_beforep.html', context)

#测试，待规范
def organizer_invite_audience(request, presentation_id):
    # 查找演讲
    presentation = get_object_or_404(Presentation, id=presentation_id)
    organizer = presentation.organizer
    # 查找所有听众用户
    all_audience = User.objects.filter(role='AUDIENCE')
    # 查找已经邀请的
    invited_ids = PresentationAttendee.objects.filter(presentation=presentation).values_list('attendee_id', flat=True)
    for user in all_audience:
        user.invited = user.id in invited_ids  # 用于模板判断已邀请

    context = {
        'presentation': presentation,
        'organizer': organizer,
        'audience_list': all_audience,
    }
    return render(request, 'presentations/before/organizer_invite_audience.html', context)

@require_POST
def invite_audience(request):
    presentation_id = request.POST.get('presentation_id')
    user_id = request.POST.get('user_id')
    # 查找并添加关联
    presentation = get_object_or_404(Presentation, id=presentation_id)
    user = get_object_or_404(User, id=user_id)
    PresentationAttendee.objects.get_or_create(presentation=presentation, attendee=user)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def remove_audience(request):
    presentation_id = request.POST.get('presentation_id')
    user_id = request.POST.get('user_id')
    PresentationAttendee.objects.filter(presentation_id=presentation_id, attendee_id=user_id).delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def organizer_invite_speaker(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    speakers = User.objects.filter(role='SPEAKER')
    if request.method == "POST":
        new_speaker_id = request.POST.get("speaker_id")
        if new_speaker_id:
            new_speaker = User.objects.get(id=new_speaker_id)
            presentation.speaker = new_speaker
            presentation.save()
            # 跳回管理页面
            return redirect(f"/presentations/manage/{presentation_id}/")
    return render(request, "presentations/before/organizer_invite_speaker.html", {
        "presentation": presentation,
        "speakers": speakers,
        "current_speaker": presentation.speaker,
    })
def preview_file(request, file_id):
    file = Upload.objects.get(id=file_id)
    return render(request, 'presentations/before/organizer_check_file.html', {'file': file})

def start_presentation(request, presentation_id):
    if request.method == 'POST':
        presentation = get_object_or_404(Presentation, id=presentation_id)
        presentation.status = 'LIVE'  # 假设你的 model 有 status 字段
        presentation.save()
        # 跳转到“演讲中”管理页面
        return redirect(f'/presentations/during/{presentation.id}/')
    else:
        # 禁止 GET 访问
        return redirect(f'/presentations/manage/{presentation_id}/')
def organizer_during_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    # ...其他上下文
    return render(request, 'presentations/during/organizer_duringp.html', {
        'presentation': presentation,
        # ...
    })
def audience_during_presentation(request):
    return render(request, "presentations/during/audience_duringp.html")