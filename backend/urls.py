from django.contrib import admin
from django.urls import path, include

from material.views import material_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # 把 core 的 URL 合并进来
    path('materials/', material_list),
]
