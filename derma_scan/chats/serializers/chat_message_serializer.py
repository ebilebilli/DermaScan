from rest_framework import serializers

from chats.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        exclude = (
            'id', 
            'user', 
            'sender'
        )
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user 
        validated_data['sender'] = ChatMessage.USER

        return super().create(validated_data)