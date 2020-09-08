import os

from django.core.mail import send_mail


def mail(subject, body, to):
    if to.type != str:
        to = [to]

    return send_mail(
        subject=subject,
        html_message=body,
        from_email=os.environ.get("EMAIL_FROM"),
        recipient_list=to,
        fail_silently=False
    )
