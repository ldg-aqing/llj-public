from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from material.views import material_list, upload_material
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('materials/', material_list, name='material_list'),
    path('upload/', upload_material, name='upload'),
    path('users/', include('users.urls')),
    path('presentations/', include('presentations.urls')),
    path('material/', include('material.urls')),
    path('api/quizzes/', include('quizzes.urls')),

    path('', lambda request: redirect('/users/login')),  # 访问 / 自动跳转到登录页
]

# 显示上传的文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)