from django.core.mail import send_mail


def send_code_by_email(user):
    username = user.username
    code = user.confirmation_code
    email = user.email
    message = (
        f'''Для регистрации на сайте пройдите по ссылке:
            http://127.0.0.1:8000/api/v1/auth/token/
            с параметрами username: "{username}" confirmation_code="{code}"
            ''')
    send_mail(
        message=message,
        subject="Регистрация пользователя",
        recipient_list=[email, ],
        from_email="registration@yamdb.ru",)