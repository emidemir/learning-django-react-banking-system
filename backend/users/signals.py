from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

from_email = settings.DEFAULT_FROM_EMAIL

from allauth.account.signals import user_signed_up

from .models import Profile

import random

User = get_user_model()

def send_simple_email(code, from_email, to_email):
    """Sends a simple email using Django's built-in send_mail function."""
    
    subject = "Backend Practice ~ Verification Code"
    message = (
        f"Your verification code is {code}"
    )

    try:
        # In future, other methodologies can be implemented.
        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False, # Set to True in production to prevent crashes
        )
    except Exception as e:
        print(f"\nAn error occurred while trying to send email: {e}")


@receiver(post_save, sender=User)
def create_user_profile(instance, sender, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Sending confirmation email
@receiver(user_signed_up) # user_signed_up is a signal defined by django-allauth.
def send_confirmation_email(user, **kwargs):
    print(user)
    code = str(random.randint(100000, 900000))
    user.verification_code = code
    send_simple_email(code, settings.DEFAULT_FROM_EMAIL, user.email)
