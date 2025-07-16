from rest_framework.decorators import api_view
from rest_framework.response import Response
from presentations.models import Presentation
from uploads.models import Upload
from .services import generate_question_from_text, save_quiz_from_ai_response

@api_view(['POST'])
def generate_ai_quiz(request, presentation_id):
    try:
        presentation = Presentation.objects.get(id=presentation_id)
        upload = Upload.objects.filter(presentation_id=presentation_id).last()
        if not upload:
            return Response({"status": "error", "message": "未找到该演讲对应的上传内容"}, status=404)

        text = upload.content
        ai_output = generate_question_from_text(text)
        quiz = save_quiz_from_ai_response(presentation, ai_output)

        return Response({
            "status": "success",
            "quiz_id": quiz.id,
            "presentation_id": presentation.id,
            "text": text,
            "output": ai_output,
            "question": quiz.question,
            "options": [
                {"id": option.id, "text": option.option_text}
                for option in quiz.options.all()
            ]
        })


    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)
