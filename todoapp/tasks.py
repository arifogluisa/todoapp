from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, msg, from_email, to_email):
    return send_mail(subject, msg, from_email, [to_email], fail_silently=False)