from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import User, Message, Conversation
from .serializers import RegisterSerializer, MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .pagination import CustomPagination
from datetime import datetime

class ALLUserViewset(ViewSet):
    http_method_names = ['get']
    queryset = User.objects.all()     
    
    def list(self, request):
        serializer = RegisterSerializer(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# MessageFilter
# django-filters
class ConversationViewSet(ViewSet, ListAPIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsParticipantOfConversation]
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()
    pagination_class = CustomPagination

    def list(self, request):
        data = Conversation.objects.filter(participants_id=request.user)
        serializer = ConversationSerializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        
# ["filters"]
#  ["conversation_id", "HTTP_403_FORBIDDEN"]
class MessageViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def list(self, request):
        data = Message.objects.filter(sender_id=request.user)
        serializer = MessageSerializer(data=data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data.get("message_body")
        message_instance = Message.objects.create(sender=request.user, message_body=message, sent_at=datetime.today())
        Conversation.objects.create(message=message_instance, participants=request.user, created_at=datetime.today())
        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
    
