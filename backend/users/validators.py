from django.core.exceptions import ValidationError

def validate_address_number(value):
    if value is not None and (value < 1 or value > 999):
        raise ValidationError('Apartment number must be between 1 and 999.')
