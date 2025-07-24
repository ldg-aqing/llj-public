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
    last_uploaded_file = ''

    if request.method == 'POST' and 'delete_id' in request.POST:
        delete_id = request.POST.get('delete_id')
        try:
            upload = Upload.objects.get(id=delete_id)
            upload.delete()
        except Upload.DoesNotExist:
            pass
        return redirect('upload_material', speaker_id=speaker_id, presentation_id=presentation_id)

    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', '').strip().lower()  # 👈 转小写
        last_uploaded_file = file.name  # ✅ 保存上传名

        # 保存临时文件
        temp_dir = 'media/temp'
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 提取文本
        extracted_text = extract_text_from_file(temp_path, file_type)

        # 保存到 Upload 模型
        Upload.objects.create(
            user_id=speaker_id,
            presentation_id=presentation_id,
            file_path=file.name,
            file_type=file_type,
            content=extracted_text
        )

        if os.path.exists(temp_path):
            os.remove(temp_path)

    materials = Upload.objects.filter(presentation_id=presentation_id).order_by('-uploaded_at')

    return render(request, 'upload.html', {
        'speaker_id': speaker_id,
        'presentation_id': presentation_id,
        'materials': materials,
        'last_uploaded_file': last_uploaded_file,
    })
