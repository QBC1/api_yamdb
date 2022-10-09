from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse

from api_yamdb.settings import PROJECT_EMAIL


def redirect_to_token(request):
    return HttpResponseRedirect(reverse('user_confrim'))


def send_code_by_email(user):
    username = user.username
    code = user.confirmation_code
    email = user.email
    message = (
        f'''Для регистрации на сайте пройдите по ссылке:
            {redirect_to_token}
            с параметрами username: "{username}" confirmation_code="{code}"
            ''')
    send_mail(
        message=message,
        subject="Регистрация пользователя",
        recipient_list=[email, ],
        from_email=PROJECT_EMAIL,)
