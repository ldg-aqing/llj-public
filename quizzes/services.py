import dashscope
from http import HTTPStatus
from django.conf import settings
import re
from .models import Quiz, QuizOption

# 模板：增加“解析”字段的要求
PROMPT_TEMPLATE = """
你是一个教育专家，请根据以下讲稿内容，生成五道有挑战性的单选题。
要求如下：
- 每道题有4个选项（A/B/C/D），只有一个是正确答案；
- 问题应基于讲稿中的核心知识点；
- 每题后请给出正确答案，并用1-2句话进行简要解析；
- 返回格式为：
题目一：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X
解析：...

题目二：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X
解析：...

题目三：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X
解析：...

题目四：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X
解析：...

题目五：
问题：
A. ...
B. ...
C. ...
D. ...
正确答案：X
解析：...

内容如下：
\"\"\"
{content}
\"\"\"
"""

def generate_question_from_text(text):
    prompt = PROMPT_TEMPLATE.format(content=text)
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding='utf-8')

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
    # 先分割为每道题的原文段落
    raw_questions = re.split(r"\s*题目[一二三四五12345]：\s*", ai_text.strip())
    quiz_list = []

    for qtext in raw_questions:
        if not qtext.strip():
            continue  # 跳过空白段

        # 提取内容
        match = re.search(
            r"问题[:：]?\s*(.*?)\s*"
            r"A[.．] (.*?)\s*"
            r"B[.．] (.*?)\s*"
            r"C[.．] (.*?)\s*"
            r"D[.．] (.*?)\s*"
            r"正确答案[:：]?\s*([ABCD])\s*"
            r"解析[:：]?\s*(.*)",
            qtext.strip(), re.DOTALL)

        if not match:
            raise ValueError("AI 返回格式错误，请检查以下文本段落：\n" + qtext)

        question, a, b, c, d, correct, explanation = match.groups()

        quiz = Quiz.objects.create(
            presentation=presentation,
            question=question.strip(),
            explanation=explanation.strip()
        )

        options = {
            'A': QuizOption.objects.create(quiz=quiz, option_text=a.strip()),
            'B': QuizOption.objects.create(quiz=quiz, option_text=b.strip()),
            'C': QuizOption.objects.create(quiz=quiz, option_text=c.strip()),
            'D': QuizOption.objects.create(quiz=quiz, option_text=d.strip()),
        }

        quiz.correct_option = options[correct.strip()]
        quiz.save()
        quiz_list.append(quiz)

    return quiz_list

