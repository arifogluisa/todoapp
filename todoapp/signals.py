from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from .tasks import send_email_task
from django.utils import timezone


@receiver(pre_save, sender = Task, dispatch_uid = 'send_notification')
def send_notification(sender, **kwargs):
    instance = kwargs.get('instance')


    delta = instance.deadline - timezone.now()
    time_left_to_deadline = delta.total_seconds()

    from_email = 'notificationtodo@gmail.com'
    to_email = 'arifogluisa@gmail.com'
    subject = (f'Task notification - {instance.title}')
    msg = ('There are 10 minutes left to deadline of your task\n'
                'Task details:\n'
                'Title: {}\n'
                'Description: {}\n'
                'Deadline: {}\n'.
                format(instance.title,
                       instance.description,
                       instance.deadline)
                )

    if 60 <= time_left_to_deadline <= 605:

        send_email_task.apply_async(
                (subject, msg, from_email, to_email),
                countdown=5,
            )
    elif time_left_to_deadline > 605:
        countdown = time_left_to_deadline - 60 * 10
        if countdown > 0:
            send_email_task.apply_async(
                    (subject, msg, from_email, to_email),
                    countdown=countdown,
                )
        else:
            send_email_task.apply_async(
                    (subject, msg, from_email, to_email),
                    countdown=5,
                )
        