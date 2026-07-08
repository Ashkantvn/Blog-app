from django.conf import settings
from django.core.mail import send_mail

from accounts.email_templates import CONFIRM_CODE_TEMPLATE


def send_confirm_code_mail(email: str, code: str):
    subject = "Your confirmation code"
    message = CONFIRM_CODE_TEMPLATE.format(code=code)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )