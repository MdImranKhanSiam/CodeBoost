import asyncio
from django.shortcuts import redirect


class BlockDirectGoogleCallbackMiddleware:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):
        callback_path = '/accounts/google/login/callback/'

        if request.user.is_authenticated and request.path == callback_path:
            return redirect('/')

        if request.path == callback_path and 'code' not in request.GET:
            return redirect('/')

        return await self.get_response(request)
