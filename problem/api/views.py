from django_ratelimit.decorators import ratelimit

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from problem.languages import LANGUAGES


@api_view(["GET"])
@ratelimit(key='user', rate='30/m', method='GET', block=True)
@permission_classes([IsAuthenticated])
def languages(request):

    return Response(LANGUAGES)





@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def ai_explain(request, problem_id):
    
    data = {"result": """There will be days when you feel tired, confused, and unsure of yourself. There will be moments when your hard work seems to produce no results, and you may wonder whether you are really good enough. But remember this: struggling does not mean you are failing. It means you are growing.

Every expert was once a beginner. Every successful person has faced rejection, failure, doubt, and countless difficult days. The difference is that they kept going when it would have been easier to quit.

You don't have to become great overnight. You just have to become a little better than you were yesterday. Learn one more thing. Solve one more problem. Take one more step. Small progress, repeated consistently, eventually becomes something extraordinary.

Don't compare your chapter one to someone else's chapter twenty. Everyone has a different journey, a different starting point, and a different timeline. Focus on your own path. Your only competition should be the person you were yesterday.

And when you fail, don't let failure define you. Learn from it. Stand up. Try again. Failure is not the opposite of success; it is part of the process that leads to success.

There will be times when nobody believes in you. That's when you need to believe in yourself the most. Keep working when nobody is watching. Keep learning when nobody is praising you. Keep moving forward even when the destination feels far away.

One day, the things you are struggling with today will become the things you are proud that you overcame.

So don't give up because it's difficult. Keep going because it's difficult. The challenges you face today are preparing you for the person you want to become tomorrow.

Your dreams are not achieved by motivation alone. They are achieved through discipline, patience, consistency, and the courage to keep going when motivation disappears.

Believe in yourself. Trust the process. Stay patient. Keep learning. Keep improving. And most importantly, never stop moving forward.

Your story is still being written, and the best chapters may still be ahead of you."""}

    return Response(data)




@api_view(["POST"])
@ratelimit(key='user', rate='30/m', method='POST', block=True)
@permission_classes([IsAuthenticated])
def ai_review(request, problem_id):
    
    data = {"result": """There will be days when you feel tired, confused, and unsure of yourself. There will be moments when your hard work seems to produce no results, and you may wonder whether you are really good enough. But remember this: struggling does not mean you are failing. It means you are growing.

Every expert was once a beginner. Every successful person has faced rejection, failure, doubt, and countless difficult days. The difference is that they kept going when it would have been easier to quit.

You don't have to become great overnight. You just have to become a little better than you were yesterday. Learn one more thing. Solve one more problem. Take one more step. Small progress, repeated consistently, eventually becomes something extraordinary.

Don't compare your chapter one to someone else's chapter twenty. Everyone has a different journey, a different starting point, and a different timeline. Focus on your own path. Your only competition should be the person you were yesterday.

And when you fail, don't let failure define you. Learn from it. Stand up. Try again. Failure is not the opposite of success; it is part of the process that leads to success.

There will be times when nobody believes in you. That's when you need to believe in yourself the most. Keep working when nobody is watching. Keep learning when nobody is praising you. Keep moving forward even when the destination feels far away.

One day, the things you are struggling with today will become the things you are proud that you overcame.

So don't give up because it's difficult. Keep going because it's difficult. The challenges you face today are preparing you for the person you want to become tomorrow.

Your dreams are not achieved by motivation alone. They are achieved through discipline, patience, consistency, and the courage to keep going when motivation disappears.

Believe in yourself. Trust the process. Stay patient. Keep learning. Keep improving. And most importantly, never stop moving forward.

Your story is still being written, and the best chapters may still be ahead of you."""}

    return Response(data)