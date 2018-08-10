import json
from functools import wraps
from django.http import JsonResponse
from json.decoder import JSONDecodeError
from .models import AuthToken


def json_call(view_func):
    @wraps(view_func)
    def wrapper_view_func(request, *args, **kwargs):
        try:
            body = request.body.decode('utf-8')
            if body == '':
                request.json = {}
            else:
                request.json = json.loads(body)
        except JSONDecodeError:
            return JsonResponse(data={'result': 'Invalid JSON! {0}'.format(body)}, status=500)

        return view_func(request, *args, **kwargs)
    return wrapper_view_func


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            body = request.body.decode('utf-8')
            try:
                params = json.loads(body)
            except JSONDecodeError:
                return JsonResponse(data={'result': 'Invalid JSON! {0}'.format(body)}, status=500)
            if 'token' not in params:
                return JsonResponse(data={'result': 'Token required!'}, status=401)

            token = params['token']
            try:
                authtoken = AuthToken.objects.get(token=token)
            except AuthToken.DoesNotExist:
                return JsonResponse(data={'result': 'Invalid token!'}, status=401)

            if not authtoken.user.has_perm(permission):
                return JsonResponse(data={'result': 'Permission denied!'}, status=401)

            return func(request, *args, **kwargs)
        return inner
    return decorator
