from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

   
year_validator = RegexValidator(
    regex=r'^(1888|18[89]\d|19\d{2}|20\d{2}|21\d{2}|22\d{2}|23\d{2}|24\d{2}|25\d{2})$',
    message='Invalid date format'
)


def validate_birthday(value):
    today = timezone.now().date()
    min_allowed_date = today - timedelta(days=365 * 200) 
    min_allowed_age = today - timedelta(days=365 * 13)
    
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%d-%m-%Y').date()
        except ValueError:
            raise ValidationError('Invalid date format. Use DD-MM-YYYY.')
    
    if value > today:
        raise ValidationError('Birthday cannot be in the future')
    
    if value > min_allowed_age:
        raise ValidationError('User must be at least 13 years old')
    
    if value < min_allowed_date:
        raise ValidationError('Birthday cannot be more than 100 years ago')
