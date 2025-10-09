from celery import shared_task
from django.core.mail import send_mail
from accounts.models import ConfirmCode
from django.contrib.auth import get_user_model
from accounts.email_templates import CONFIRM_CODE_TEMPLATE
from accounts.utils import generate_random_string

from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task(bind=True, max_retries=3)
def send_confirm_code_mail(self, email):
    try:
        user = User.objects.filter(email=email).first()
        if not user:
            return
        code = generate_random_string(12)
        ConfirmCode.objects.update_or_create(
            user=user,
            defaults={"code": code},
        )
        message = CONFIRM_CODE_TEMPLATE.format(code=code)
        # Send mail
        send_mail(
            subject="Your confirm code!",
            message=message,
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as exception:
        self.retry(exc=exception, countdown=30)


@shared_task
def delete_expired_confirm_codes():
    target_time = timezone.now() - timedelta(minutes=3)
    ConfirmCode.objects.filter(created_date__lt=target_time).delete()
