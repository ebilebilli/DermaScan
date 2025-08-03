from rest_framework import serializers

from chats.models import ChatMessage


class CreateChatMessageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        exclude = (
            'id', 
            'user', 
            'sender',
            'image',
        )
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user 
        validated_data['sender'] = ChatMessage.USER
        return super().create(validated_data)
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None