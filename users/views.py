from django.shortcuts import render


def login_view(request):
    return render(request, 'login.html')  # 渲染登录模板


def register_view(request):
    return render(request, 'register.html')  # 渲染注册模板


from django.shortcuts import render

# Create your views here.
