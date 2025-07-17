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
        speaker_id = int(request.POST.get('speaker_id'))
        presentation_id = int(request.POST.get('presentation_id'))

        # ✅ 临时保存文件以供提取
        temp_dir = 'media/temp'
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.name)

        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # ✅ 提取文本内容
        extracted_text = extract_text_from_file(temp_path, file_type)

        # ✅ 写入 Upload 模型（包含提取内容）
        Upload.objects.create(
            user_id=speaker_id,
            presentation_id=presentation_id,
            file_path=file.name,
            file_type=file_type,
            content=extracted_text
        )

        # ✅ 可选写入 UploadedMaterial（用于 material_list）
        UploadedMaterial.objects.create(
            title=file.name,
            file=file,
            file_type=file_type,
            extracted_text=extracted_text
        )

        # ✅ 删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return render(request, 'upload.html', {
            'form': UploadForm(),
            'speaker_id': speaker_id,
            'presentation_id': presentation_id,
            'success': '上传成功并提取完毕！'
        })

    else:
        form = UploadForm()
    return render(request, 'upload.html', {
        'form': form,
        'speaker_id': speaker_id,
        'presentation_id': presentation_id,
    })
