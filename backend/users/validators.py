from rest_framework.validators import ValidationError
from django.utils import timezone
from datetime import date

def validate_user_age(value):
    today = timezone.now().date()
    
    if value > today:
        raise ValidationError('The date of birth cannot be in the future.')
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('You must be at least 18 years old.')
    

