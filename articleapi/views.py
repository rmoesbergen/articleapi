from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.http import require_POST, require_GET
from .models import AuthToken, Article
from datetime import datetime, timedelta
from .decorators import json_call
import uuid


@require_POST
@json_call
def v1_login(request):
    params = request.json
    if 'username' not in params or 'password' not in params:
        return JsonResponse(data={'result': 'required field is missing! {0}'.format(params)}, status=401)

    user = authenticate(request, username=params['username'], password=params['password'])
    if user:
        # Check for existing auth token for this user
        try:
            authtoken = AuthToken.objects.get(pk=user)
        except AuthToken.DoesNotExist:
            # Create new token and save
            token = str(uuid.uuid4()).replace('-', '')
            authtoken = AuthToken(user=user, token=token, expires=datetime.now() + timedelta(hours=24))
            authtoken.save()
    else:
        return JsonResponse(data={'result': 'permission denied!'}, status=401)

    result = {'result': 'ok', 'token': authtoken.token}
    return JsonResponse(data=result)


@require_GET
@json_call
def v1_articles(request):
    articles = Article.objects.all()

    arts = []
    for article in articles:
        art = {
            article.id: {
                "subject": article.subject,
                "author": article.author,
            }
        }
        arts.append(art)

    result = {'result': 'ok',
              'articles': arts}

    return JsonResponse(data=result)


def v1_article(request, articleid):
    try:
        article = Article.objects.get(pk=articleid)
    except Article.DoesNotExist:
        return JsonResponse(data={'result': 'No such article!'})

    result = {
        'result': 'ok',
        'article': {
            'id': article.id,
            'subject': article.subject,
            'body': article.body,
            'author': article.author
        }
    }

    return JsonResponse(data=result)
