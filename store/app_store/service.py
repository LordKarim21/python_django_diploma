from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Вы оплатили',
        'mail',
        'username@gmail.com',
        [user_email],
        fail_silently=False,
    )
