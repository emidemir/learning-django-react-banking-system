from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .validators import validate_user_age
import datetime


# pip install "django-phonenumber-field[phonenumbers]"
# https://github.com/stefanfoulis/django-phonenumber-field?tab=readme-ov-file
from phonenumber_field.modelfields import PhoneNumberField 
# pip install django-countries
# https://pypi.org/project/django-countries/
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'
        NOT_SPECIFIED = 'NOT_SPECIFIED', 'Not Specified'
    
    gender = models.CharField(
        max_length=13, 
        choices=Gender.choices, 
        default=Gender.NOT_SPECIFIED
    )
    
    # For KYC (Know Your Customer) - important for banking!
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=False, null=True)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    
    # The filename parameter is taken directly from the uploaded file object.
    # it’s the original name of the file as provided by the user when they uploaded it.
    return "users/{0}/{1}".format(instance.user.username, filename)

class Profile(models.Model):
    user = models.ForeignKey(CustomUser, related_name='profile', on_delete=models.CASCADE) # Don't forget related name for reverse lookup. user_instance.<related_name>_set.all()
    avatar = models.ImageField(upload_to=user_directory_path, default='default.jpg', blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, default="99999999999")
    date_of_birth = models.DateField(blank=False, null=False, default=datetime.datetime.now, validators=[validate_user_age])
    
class Address(models.Model):
    user = models.ForeignKey(CustomUser, related_name="addresses", on_delete=models.CASCADE)
    country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    building_number = models.IntegerField(
        blank=True, null=True, validators=[
            MinLengthValidator(1, 'Building number can\'t be negative'),
            MaxLengthValidator(99, 'Building number can\'t be more than 99')
        ]
    )
    apartment_number = models.IntegerField(
        blank=True, null=True, validators=[
            MinLengthValidator(1, 'Apartment number can\'t be negative'),
            MaxLengthValidator(99, 'Apartment number can\'t be more than 99')
        ]
    )
