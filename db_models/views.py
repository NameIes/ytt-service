import uuid
import datetime

from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

from db_models.models import EmailVerificationCode


def login(request):
    if request.method == 'GET':
        return render(request, 'custom_admin/login.html')
    if request.method != 'POST':
        raise Http404()

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    if not username or not password:
        return render(request, 'custom_admin/login.html', {'message': 'Заполните все поля для входа.'})

    if not User.objects.filter(username=username).exists():
        return render(request, 'custom_admin/login.html', {'message': 'Неверно указаны данные для входа.'})

    user_obj = User.objects.get(username=username)
    if not user_obj.check_password(password):
        return render(request, 'custom_admin/login.html', {'message': 'Неверно указаны данные для входа.'})

    email_code = EmailVerificationCode(
        user=user_obj,
        code=uuid.uuid4().hex.upper()[:24],
        valid_until=datetime.datetime.now() + datetime.timedelta(minutes=15),
    )
    email_code.save()

    send_mail(
        'Подтверждение почты',
        'Для подтверждения почты перейдите по ссылке: ' + request.build_absolute_uri(
            email_code.get_code_url()
        ),
        None,
        [user_obj.email],
        fail_silently=False,
    )

    return render(request, 'custom_admin/login.html', {'message': 'На вашу почту отправлена ссылка для входа.'})

def confirm_email(request, user_id, code):
    if not User.objects.filter(id=user_id).exists():
        raise Http404()

    user_obj = User.objects.get(id=user_id)
    if not EmailVerificationCode.objects.filter(user=user_obj, code=code).exists():
        raise Http404()

    django_login(request, user_obj)

    code_obj = EmailVerificationCode.objects.get(user=user_obj, code=code)
    code_obj.delete()

    return HttpResponseRedirect('/admin/')
