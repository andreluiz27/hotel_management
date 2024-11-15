from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, data, message, sender, receiver):
    try:
        send_mail(
            subject,
            message,
            sender,
            receiver,
            fail_silently=False,
        )
    except Exception as e:
        print(e)
        return False
    return True
