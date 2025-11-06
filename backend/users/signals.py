from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

from django.core.mail import send_mail

from .models import Profile
import random

from allauth.account.signals import user_signed_up

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(instance, sender, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Sending confirmation email
@receiver(user_signed_up) # user_signed_up is a signal defined by django-allauth.
def send_confirmation_email(user, **kwargs):
    code = str(random.randint(100000, 900000))
    user.verification_code = code
    send_mail(
        subject=code,
        message=f"Your verification code is {code}",
        from_email="emirhan.2521demir@gmail.com",
        recipient_list=[user.email],
        fail_silently=False
    )
