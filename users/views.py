from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Users

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('password_confirm')
            Users.objects.create(**form.cleaned_data)
            messages.success(request, "注册成功，请登录")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['role'] = user.role

            if user.role == 'ORGANIZER':
                return redirect('/users/organizer/')
            elif user.role == 'SPEAKER':
                return redirect('/users/speaker/')
            elif user.role == 'AUDIENCE':
                return redirect('/users/audience/')
        except Users.DoesNotExist:
            messages.error(request, "用户名或密码错误")

    return render(request, 'login.html')