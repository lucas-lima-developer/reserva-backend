from django.forms import ValidationError
from rest_framework import serializers
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta: 
        model = User
        fields = ('email', 'password')

    def create(self, validate_data):
        email = validate_data.get('email')
        password = validate_data.get('password')

        try:
            validate_email(email)
        except ValidationError:
            raise DRFValidationError('Invalid email adress.')
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise DRFValidationError(str(e))
        
        user = User.objects.create_user(
            email=email,
            password=password
        )

        return user
