from django.db import models
from django.contrib.auth.models import User

from .validators import validate_address_number


# pip install "django-phonenumber-field[phonenumbers]"
# https://github.com/stefanfoulis/django-phonenumber-field?tab=readme-ov-file
from phonenumber_field.modelfields import PhoneNumberField 
# pip install django-countries
# https://pypi.org/project/django-countries/
from django_countries.fields import CountryField

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    
    # The filename parameter is taken directly from the uploaded file object.
    # it’s the original name of the file as provided by the user when they uploaded it.
    return "users/{0}/{1}".format(instance.user.username, filename)

class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE) # Don't forget related name for reverse lookup. user_instance.<related_name>_set.all()
    avatar = models.ImageField(upload_to=user_directory_path, default='default.jpg', blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    birth_day = models.DateField(blank=False, null=False, auto_now_add=True) # auto_now_add=True because this project won't go to production


    class Gender(models.TextChoices):
        MALE = 'MALE', 'male'
        FEMALE = 'FEMALE', 'female'
        OTHER = 'OTHER', 'other'
        NOT_SPECIFIED = 'NOT_SPECIFIED', 'not specified' # DEFAULT
    
    gender = models.CharField(max_length=13, choices=Gender.choices, default=Gender.NOT_SPECIFIED)

class Address(models.Model):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    country = CountryField(blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    district = models.CharField(max_length=100, blank=False, null=False)
    street_address = models.CharField(max_length=250, blank=False, null=False)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    primary = models.BooleanField(default=False)
    phone_number = PhoneNumberField(null=True, blank=True)
    building_number = models.IntegerField(
        blank=True, null=True, validators=[validate_address_number(1)]
    )
    apartment_number = models.IntegerField(
        blank=True, null=True, validators=[validate_address_number(1)]
    )
