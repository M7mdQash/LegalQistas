import logging

from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def notify_new_message(session, message):
    recipient = session.customer if message.sender == session.lawyer else session.lawyer
    if not recipient.email:
        return
    try:
        send_mail(
            subject=f'New message in your session #{session.pk}',
            message=message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Failed to send message notification for session #%s to %s",
            session.pk,
            recipient.email,
        )
