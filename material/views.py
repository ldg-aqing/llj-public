# material/views.py
import os
from django.shortcuts import render, redirect
from .models import UploadedMaterial
from .forms import UploadForm
from .utils import extract_text_from_file

ALLOWED_EXT = ['pptx', 'pdf']  # 限制上传类型

def material_list(request):
    materials = UploadedMaterial.objects.all()
    return render(request, 'material_list.html', {'materials': materials})

def upload_material(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            ext = os.path.splitext(instance.file.name)[1][1:].lower()
            if ext not in ALLOWED_EXT:
                return render(request, 'upload.html', {'form': form, 'error': '仅支持 pptx 和 pdf 文件上传。'})

            instance.file_type = ext
            instance.save()

            file_path = instance.file.path
            print("提取文字文件路径（已保存）是：", file_path)

            extracted = extract_text_from_file(file_path, ext)
            instance.extracted_text = extracted
            instance.save()

            print("接收到文件：", instance.file.name)
            try:
                print("提取文字内容为：", extracted.encode('gbk', errors='ignore').decode('gbk'))
            except UnicodeEncodeError:
                print("提取文字内容包含无法显示的字符（已忽略）")

            return redirect('upload')
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
