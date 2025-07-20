from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def handle_form(request):
    # 注册逻辑
    if request.method == 'POST' and 'form_type' in request.POST and request.POST['form_type'] == 'register':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role')

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, "用户名已存在")
            return render(request, 'log/login.html')

        # 检查密码是否一致
        if password != password_confirm:
            messages.error(request, "密码不一致")
            return render(request, 'log/login.html')

        # 创建用户
        try:
            User.objects.create(
                username=username,
                email=email,
                password=password,  # 注意：实际项目中应该加密存储
                role=role
            )
            messages.success(request, "注册成功，请登录")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"注册失败: {str(e)}")
            return render(request, 'log/login.html')

    # 登录逻辑
    elif request.method == 'POST' and 'form_type' in request.POST and request.POST['form_type'] == 'login':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)  # 注意：密码应加密验证
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == 'ORGANIZER':
                return redirect('/presentations/organizer/')
            elif user.role == 'SPEAKER':
                return redirect('/presentations/speaker/')
            elif user.role == 'AUDIENCE':
                return redirect('/presentations/audience/')
        except User.DoesNotExist:
            messages.error(request, "用户名或密码错误")

    # GET请求时返回页面
    return render(request, 'log/login.html')