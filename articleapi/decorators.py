import json
from functools import wraps
from django.http import JsonResponse
from json.decoder import JSONDecodeError


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
