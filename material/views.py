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
    from .models import UploadedMaterial
    from django.views.decorators.csrf import csrf_exempt

    # 处理删除请求
    if request.method == 'POST' and 'delete_id' in request.POST:
        delete_id = request.POST.get('delete_id')
        try:
            material = UploadedMaterial.objects.get(id=delete_id)
            if material.file:
                file_path = material.file.path
                if os.path.exists(file_path):
                    os.remove(file_path)
            material.delete()
        except UploadedMaterial.DoesNotExist:
            pass
        return redirect('upload_material', speaker_id=speaker_id, presentation_id=presentation_id)

    # 处理上传请求
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', '').lower()
        speaker_id = int(request.POST.get('speaker_id'))
        presentation_id = int(request.POST.get('presentation_id'))

        temp_dir = 'media/temp'
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.name)

        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        extracted_text = extract_text_from_file(temp_path, file_type)

        Upload.objects.create(
            user_id=speaker_id,
            presentation_id=presentation_id,
            file_path=file.name,
            file_type=file_type,
            content=extracted_text
        )

        UploadedMaterial.objects.create(
            title=file.name,
            file=file,
            file_type=file_type,
            extracted_text=extracted_text
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)

    # 获取当前上传内容列表
    materials = UploadedMaterial.objects.all()
    return render(request, 'upload.html', {
        'form': UploadForm(),
        'speaker_id': speaker_id,
        'presentation_id': presentation_id,
        'materials': materials,
    })
