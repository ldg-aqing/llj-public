import dashscope
from http import HTTPStatus
from django.conf import settings
import re
from .models import Quiz, QuizOption

# 模板：可根据你要生成的内容进一步优化
PROMPT_TEMPLATE = """
你是一个教育专家，请根据以下讲稿内容，生成五道有挑战性的单选题。
要求如下：
- 每道题有4个选项（A/B/C/D），只有一个是正确答案；
- 问题应基于讲稿中的核心知识点；
- 返回格式为：
题目一：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X

题目二：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X

题目三：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X

题目四：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X

题目五：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X

内容如下：
\"\"\"
{content}
\"\"\"
"""

def generate_question_from_text(text):
    prompt = PROMPT_TEMPLATE.format(content=text)
    print("发送给 AI 的 prompt 是：\n", prompt)

    response = dashscope.Generation.call(
        model='qwen-turbo',
        messages=[{"role": "user", "content": prompt}],
        result_format='message',
        api_key=settings.DASHSCOPE_API_KEY
    )

    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        raise RuntimeError("Qwen 调用失败：" + str(response))

def save_quiz_from_ai_response(presentation, ai_text):
    # 正则匹配 AI 返回格式
    pattern = r"问题[:：]?\s*(.*?)\s*A[.．] (.*?)\s*B[.．] (.*?)\s*C[.．] (.*?)\s*D[.．] (.*?)\s*正确答案[:：]?\s*([ABCD])"
    matches = re.findall(pattern, ai_text, re.DOTALL)

    if not matches:
        raise ValueError("AI 返回格式错误，请检查模型输出")

    quiz_list = []
    for match in matches:
        question, a, b, c, d, correct = match
        quiz = Quiz.objects.create(presentation=presentation, question=question)

        options = {
            'A': QuizOption.objects.create(quiz=quiz, option_text=a),
            'B': QuizOption.objects.create(quiz=quiz, option_text=b),
            'C': QuizOption.objects.create(quiz=quiz, option_text=c),
            'D': QuizOption.objects.create(quiz=quiz, option_text=d),
        }

        quiz.correct_option = options[correct]
        quiz.save()
        quiz_list.append(quiz)

    return quiz_list
