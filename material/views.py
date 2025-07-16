# material/views.py
import os
from django.shortcuts import render, redirect
from .models import UploadedMaterial
from .forms import UploadForm
from .utils import extract_text_from_file
# 引入 Upload 模型
from uploads.models import Upload
ALLOWED_EXT = ['pptx', 'pdf']  # 限制上传类型

def material_list(request):
    materials = UploadedMaterial.objects.all()
    return render(request, 'material_list.html', {'materials': materials})


def upload_material(request, speaker_id, presentation_id):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type')
        speaker_id = request.POST.get('speaker_id')
        presentation_id = request.POST.get('presentation_id')

        # 保存 Upload 模型（uploads/models.py 中）
        Upload.objects.create(
            user_id=speaker_id,
            presentation_id=presentation_id,
            file_path=file.name,
            file_type=file_type
        )

        return render(request, 'upload.html', {
            'form': UploadForm(),  # 重新渲染一个空表单
            'speaker_id': speaker_id,
            'presentation_id': presentation_id,
            'success': '上传成功！'
        })

    # GET 请求时，渲染上传页面，传入 speaker_id 和 presentation_id
    else:
        form = UploadForm()
    return render(request, 'upload.html', {
        'form': form,
        'speaker_id': speaker_id,
        'presentation_id': presentation_id,
    })