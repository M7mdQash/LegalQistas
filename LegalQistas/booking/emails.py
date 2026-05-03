from django.core.mail import send_mail
from django.conf import settings


def notify_new_message(session, message):
    recipient = session.customer if message.sender == session.lawyer else session.lawyer
    send_mail(
        subject=f'New message in your session #{session.pk}',
        message=message.body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        fail_silently=True,
    )
