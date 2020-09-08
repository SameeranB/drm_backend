import os

from django.core.mail import send_mail


def mail(subject, body, to):

    return send_mail(
        subject=subject,
        message=body,
        from_email=os.environ.get("EMAIL_FROM"),
        recipient_list=[to],
        fail_silently=False
    )
