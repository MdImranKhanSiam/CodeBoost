import json, os
from django_ratelimit.decorators import ratelimit

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from problem.languages import LANGUAGES
from . services import PROMPTS, build_prompt

from openai import OpenAI
from groq import Groq

@api_view(["GET"])
@ratelimit(key='user', rate='30/m', method='GET', block=True)
@permission_classes([IsAuthenticated])
def languages(request):

    return Response(LANGUAGES)





@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def ai_explain(request, problem_id):
    
    prompt = build_prompt(problem_id)

    groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
    )

    result = response.choices[0].message.content

    # openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # response = openai_client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {
    #             "role": "user", 
    #             "content": prompt
    #         }
    #     ],
    #     max_tokens=1500,
    # )

    # result = response.choices[0].message.content

    print(result)

    data = {}

    data['result'] = result

    return Response(data)




@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def ai_review(request, problem_id):
    
    data = {"result": """There will be days when you feel tired, confused, and unsure of yourself. There will be moments when your hard work seems to produce no results, and you may wonder whether you are really good enough. But remember this: struggling does not mean you are failing. It means you are growing.

Your story is still being written, and the best chapters may still be ahead of you."""}

    body = request.data.copy()
    code = body['code'].strip()
    language = body['language'].strip()

    print(problem_id)
    print(code)
    print(language)

    return Response(data)