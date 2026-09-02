import json, os
from django_ratelimit.decorators import ratelimit

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from problem.languages import LANGUAGES
from . services import build_explain_prompt, build_review_prompt
from . ai_services import call_groq

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
    prompt = build_explain_prompt(problem_id)

    try:
        result = call_groq(prompt)
    except RuntimeError:
        return Response(
            {"error": "AI is rate limited right now, please try again in a bit."},
            status=429,
        )

    data = {}

    data['result'] = result

    return Response(data)




@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def ai_review(request, problem_id):
    body = request.data.copy()
    language = body['language'].strip()
    code = body['code'].strip()

    prompt = build_review_prompt(problem_id, language, code)

    try:
        result = call_groq(prompt)
    except RuntimeError:
        return Response(
            {"error": "AI is rate limited right now, please try again in a bit."},
            status=429,
        )

    data = {}

    data['result'] = result

    return Response(data)