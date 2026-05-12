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

