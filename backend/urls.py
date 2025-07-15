from django.contrib import admin
from django.urls import path, include

from material.views import material_list, upload_material
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('materials/', material_list, name='material_list'),
    path('upload/', upload_material, name='upload'),
]

# 显示上传的文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)