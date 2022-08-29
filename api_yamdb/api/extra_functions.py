from django.core.mail import send_mail

from api_yamdb.settings import PROJECT_EMAIL, URL_FOR_GET_TOKEN


def send_code_by_email(user):
    username = user.username
    code = user.confirmation_code
    email = user.email
    message = (
        f'''Для регистрации на сайте пройдите по ссылке:
            {URL_FOR_GET_TOKEN}
            с параметрами username: "{username}" confirmation_code="{code}"
            ''')
    send_mail(
        message=message,
        subject="Регистрация пользователя",
        recipient_list=[email, ],
        from_email=PROJECT_EMAIL,)
