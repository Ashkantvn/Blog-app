from django.conf import settings
from django.core.mail import send_mail
from django.tasks import task

from accounts.email_templates import CONFIRM_CODE_TEMPLATE

@task
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