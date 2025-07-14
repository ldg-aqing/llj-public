from django.contrib import admin
from django.urls import path, include

from material.views import material_list, upload_material
from users.views import login_view, register_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # 把 core 的 URL 合并进来
    path('materials/', material_list, name='material_list'),
    path('upload/', upload_material, name='upload'),

    path('login/', login_view, name='login'),          # 登录页
    path('register/', register_view, name='register'), # 注册页
]

# 显示上传的文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)