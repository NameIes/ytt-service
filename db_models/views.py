import requests
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def send(request):
    requests.post('https://crk-31.ru/api/post/', json={'test': 'test'})
    return HttpResponse('Ok')


@login_required()
def index(request):
    pass
