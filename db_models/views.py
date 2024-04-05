import requests
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


def send(request):
    requests.post('https://crk-31.ru/api/post/', json={'test': 'test'})
    return HttpRequest('Ok')


@login_required()
def index(request):
    pass
