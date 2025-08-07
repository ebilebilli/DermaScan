from rest_framework import serializers

from scans.models import SkinImage


class SkinImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SkinImage
        exclude = (
            'user',
            'uploaded_at',
            'is_analyzed'
        )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user 
        return super().create(validated_data)
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None