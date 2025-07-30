from PIL import Image
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models.user import CustomerUser


__all__ = [
    'ProfileSerializer',
    'ProfileDetailSerializer',
    'ProfileUpdateSerializer'
]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        exclude = ['id', 'bio', 'email', 'birthday']

    def validate_profile_image(self, image):
        valid_formats = ['JPEG', 'JPG', 'PNG']
        max_size = 2 * 1024 * 1024  

        if image.size > max_size:
            raise serializers.ValidationError('Image size should not exceed 2 MB.')
        
        try:
            img = Image.open(image)
            if img.format.upper() not in valid_formats:
                raise serializers.ValidationError(f"Image format must be one of: {', '.join(valid_formats)}.")
        except Exception:
            raise serializers.ValidationError('Invalid image file')

        return image

 
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
            'bio', 'profile_image'
            )
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'birthday': {'required': False},
            'bio': {'required': False},
            'profile_image': {'required': False},
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
        actual.bio = validated_data.get('bio', actual.bio)
        actual.profile_image = validated_data.get('profile_image', actual.profile_image)

        if 'password' in validated_data:
            actual.set_password(validated_data['password'])  
            
        actual.save()
    
        return actual