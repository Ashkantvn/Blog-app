from celery import shared_task
from django.core.mail import send_mail
import random, string
from accounts.models import ConfirmCode
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

User = get_user_model()

def generate_random_string(length=12):
    characters = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(random.choices(characters, k=length))

@shared_task
def send_confirm_code_mail(email):
    user = User.objects.filter(email=email).first()
    code = generate_random_string(12)
    domain = 'http://localhost:8000' # Change it in production
    reset_confirm_url = reverse("accounts:reset-confirm",args=[code])
    ConfirmCode.objects.create(
        code=code,
        user=user,
    )
    # Send mail
    send_mail(
        subject='Your confirm code!',
        message= domain + reset_confirm_url,
        from_email='noreply@example.com',
        recipient_list=[email],
        fail_silently=False,
    )