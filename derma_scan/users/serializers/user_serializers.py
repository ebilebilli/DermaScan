from PIL import Image
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models.user import CustomerUser


__all__ = [
    'ProfileDetailSerializer',
    'ProfileUpdateSerializer'
]

class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'


class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    password_two = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomerUser
        fields = (
            'email', 'username', 
            'password', 'password_two', 'birthday',
            )
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'birthday': {'required': False}
        }
        
    def validate(self, data):
        if 'password' in data or 'password_two' in data:
            if data['password'] != data['password_two']:
                raise serializers.ValidationError('Passwords must match')
        return data
        
    def update(self, actual, validated_data):
        validated_data.pop('password_two', None)

        actual.email = validated_data.get('email', actual.email)
        actual.username = validated_data.get('username', actual.username)
        actual.birthday = validated_data.get('birthday', actual.birthday)

        if 'password' in validated_data:
            actual.set_password(validated_data['password'])  
            
        actual.save()
    
        return actual