from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from .models import User, Conversation, Message

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=255, min_length=3)
    last_name = serializers.CharField(max_length=255, min_length=3)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=16, allow_blank=True, required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    created_at = serializers.DateTimeField(read_only=True)   

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("This field cannot be blank")
        if value and len(value) < 8:
            raise serializers.ValidationError("Password length should be greater than or equal to 8")
        return value.strip()
    
class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
class MessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField(read_only=True)
    sender = serializers.UUIDField(read_only=True)
    message_body = serializers.CharField(max_length=255)
    sent_at = serializers.DateTimeField(read_only=True)

class ConversationSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField(format="hex_verbose", read_only=True)
    participant = serializers.UUIDField(format="hex_verbose", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    message = MessageSerializer()
    message_count = serializers.SerializerMethodField()

    def get_message_count(self, obj):
        # Assuming `obj` has a related_name 'messages' for Message model
        return obj.messages.count()
    