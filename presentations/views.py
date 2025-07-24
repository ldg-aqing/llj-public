from django.contrib.auth.decorators import login_required
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated
import logging
from users.models import User
from django.shortcuts import render, get_object_or_404, redirect
from presentations.models import Presentation, PresentationAttendee
from material.forms import UploadForm
from uploads.models import Upload
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from quizzes.models import Quiz, QuizOption, QuizSession
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.csrf import csrf_exempt
from feedback.models import Feedback
from discussions.models import Discussion, Comment
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

    # --- 加入排序 ---
    from django.db.models import Case, When, Value, IntegerField
    status_order = Case(
        When(status='LIVE', then=Value(0)),
        When(status='PENDING', then=Value(1)),
        When(status='FINISHED', then=Value(2)),
        default=Value(99),
        output_field=IntegerField(),
    )
    presentations = (
        Presentation.objects
        .filter(organizer=user)
        .annotate(status_order=status_order)
        .order_by('status_order', '-id')
    )

    speakers = User.objects.filter(role='SPEAKER')

    return render(request, 'users/organizer.html', {
        'user': user,
        'presentations': presentations,
        'speakers': speakers
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
    # 获取演讲
    presentation = get_object_or_404(Presentation, id=presentation_id)

    # 获取组织者、演讲者、听众，假定模型有相应字段
    organizer = presentation.organizer  # User对象
    speaker = presentation.speaker  # User对象
    attendees = PresentationAttendee.objects.filter(presentation=presentation)
    feedbacks = Feedback.objects.filter(presentation=presentation)

    return render(request, 'presentations/during/organizer_duringp.html', {
        'presentation': presentation,
        'organizer': organizer,
        'speaker': speaker,
        'attendees': attendees,
        'feedbacks': feedbacks,
    })

def audience_during_presentation(request, presentation_id):
    # 只传id到模板，其它数据前端AJAX获取
    return render(request, "presentations/during/audience_duringp.html", {"presentation_id": presentation_id})

@api_view(['GET'])
def audience_presentation_detail(request, presentation_id):
    user_id = request.GET.get('user_id')  #  从前端 URL 参数获取
    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None

    try:
        presentation = Presentation.objects.get(id=presentation_id)
        quizzes = Quiz.objects.filter(presentation_id=presentation_id, status__in=['active', 'completed']).annotate(
            status_order=Case(
                When(status='active', then=0),
                When(status='completed', then=1),
                default=2,
                output_field=IntegerField(),
            )
        ).order_by('status_order', '-id')  # 先按状态，再按id倒序
        feedbacks = Feedback.objects.filter(presentation_id=presentation_id)

        def get_correct_option_label(quiz):
            if not quiz.correct_option:
                return ""
            options = list(quiz.options.all())
            try:
                idx = options.index(quiz.correct_option)
                return chr(65 + idx)  # A,B,C,D
            except Exception:
                return ""

        question_list = []
        for q in quizzes:
            user_answer = None

            if user:
                session = QuizSession.objects.filter(quiz=q, user=user).first()
                if session and session.selected_option:
                    options = list(q.options.all())
                    try:
                        idx = options.index(session.selected_option)
                        label = chr(65 + idx)
                    except:
                        label = ''
                    user_answer = {
                        "option_id": session.selected_option.id,
                        "option_text": f"{label}. {session.selected_option.option_text}"
                    }

            question_list.append({
                "id": q.id,
                "title": f"题目 #{q.id}",
                "status": q.status,
                "content": q.question,
                "options": [
                    {"id": opt.id, "text": f"{chr(65 + i)}. {opt.option_text}"}
                    for i, opt in enumerate(q.options.all())
                ],
                "answer": f"{get_correct_option_label(q)}. {q.correct_option.option_text}" if q.correct_option else "",
                "explanation": q.explanation or "",
                "discussions": [],
                "user_answer": user_answer  # ✅ 用于前端显示“我的答案”
            })

        data = {
            "presentation": {
                "id": presentation.id,
                "title": presentation.title,
                "organizer": presentation.organizer.username if hasattr(presentation.organizer, "username") else str(
                    presentation.organizer),
                "speaker": presentation.speaker.username if hasattr(presentation.speaker, "username") else str(
                    presentation.speaker),
                "attendee_count": PresentationAttendee.objects.filter(presentation_id=presentation.id).count(),  # 这里
            },
            "feedbacks": [
                {
                    "id": fb.id,
                    "content": fb.reason,   # 这里用reason
                    "user": fb.user.username,
                    "time": fb.submitted_at.strftime('%Y-%m-%d %H:%M')
                }
                for fb in feedbacks
            ],
            "questions": question_list
        }
        return Response(data)
    except Presentation.DoesNotExist:
        return Response({"error": "演讲不存在"}, status=404)

@csrf_exempt
@api_view(['POST'])
def submit_answer_api(request):
    # 1. 先尝试用 Django 的 session 认证用户
    user = request.user
    if not user.is_authenticated:
        # 2. session 没有，再看 POST 里有没有 user_id
        user_id = request.data.get('user_id')
        if not user_id:
            # 3. 两种方式都没有用户信息，直接返回未登录
            return Response({'error': '用户未登录'}, status=403)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': '用户不存在'}, status=404)

    # 后面就可以放心使用 user 变量，不会为 None
    quiz_id = request.data.get('quiz_id')
    option_id = request.data.get('option_id')
    if not (quiz_id and option_id):
        return Response({'error': '参数不全'}, status=400)
    try:
        quiz = Quiz.objects.get(id=quiz_id)
        option = QuizOption.objects.get(id=option_id)
    except (Quiz.DoesNotExist, QuizOption.DoesNotExist):
        return Response({'error': '题目或选项不存在'}, status=404)

    session, created = QuizSession.objects.update_or_create(
        quiz=quiz,
        user=user,
        defaults={
            'selected_option': option,
            'is_correct': (option == getattr(quiz, 'correct_option', None)),
        }
    )
    return Response({'success': True, 'is_correct': session.is_correct ,
                     'selected_option_id': option.id,})




def audience_after_view(request, presentation_id, user_id):
    # 获取演讲对象
    presentation = get_object_or_404(Presentation, id=presentation_id)
    # 根据 user_id 获取用户对象
    user = get_object_or_404(User, id=user_id)

    # 获取该演讲所有反馈（如果需要过滤公开，确保category值正确）
    feedbacks = Feedback.objects.filter(presentation=presentation)

    # 获取该演讲的所有题目
    quizzes = Quiz.objects.filter(presentation=presentation).order_by('id')
    # 获取该用户针对这些题目的答题记录
    user_sessions = QuizSession.objects.filter(user=user, quiz__in=quizzes)

    quiz_data = []
    for quiz in quizzes:
        # 获取题目所有选项并标记 A B C D ...
        options = QuizOption.objects.filter(quiz=quiz).order_by('id')
        option_list = []
        for i, opt in enumerate(options):
            option_list.append({
                'label': chr(65 + i),  # 'A', 'B', 'C', 'D'
                'text': opt.option_text,
                'id': opt.id,
            })

        # 获取该用户这题的答题记录
        session = user_sessions.filter(quiz=quiz).first()

        # 找用户选项对应的字母
        selected_label = None
        if session and session.selected_option:
            for opt in option_list:
                if opt['id'] == session.selected_option.id:
                    selected_label = opt['label']
                    break

        # 找正确选项对应的字母
        correct_label = None
        if quiz.correct_option:
            for opt in option_list:
                if opt['id'] == quiz.correct_option.id:
                    correct_label = opt['label']
                    break

        # 拼接显示文字
        selected_option_text = (selected_label + ". " if selected_label else "") + (
            session.selected_option.option_text if session and session.selected_option else "")
        correct_option_text = (correct_label + ". " if correct_label else "") + (
            quiz.correct_option.option_text if quiz.correct_option else "")

        # 关联查询该题对应的讨论和评论
        try:
            discussion = Discussion.objects.get(quiz=quiz)
            comments = Comment.objects.filter(discussion=discussion).order_by('created_at')
        except Discussion.DoesNotExist:
            comments = []

        quiz_data.append({
            'quiz': quiz,
            'options': option_list,
            'selected_option_text': selected_option_text,
            'correct_option_text': correct_option_text,
            'is_correct': session.is_correct if session else None,
            'explanation': quiz.explanation or "",
            'comments': comments,  # 评论列表
        })

    context = {
        'presentation': presentation,
        'feedbacks': feedbacks,
        'quiz_data': quiz_data,
    }

    return render(request, 'presentations/after/audience_afterp.html', context)
