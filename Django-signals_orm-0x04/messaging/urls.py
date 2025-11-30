from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterViewSet, MessageModelViewSet, LoginViewset, UserViewSet, MessageHistoryModelViewSet,delete_user

app_name = 'messaging'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginViewset.as_view(), name='login'),
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='users'),
    path('user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}),name='user'),
    path('messages/', MessageModelViewSet.as_view({
                                'post': 'create', 'get': 'list'
                                }), name='messages'),
    path('message/<int:pk>/', MessageModelViewSet.as_view({
                                'get': 'retrieve', 'patch': 'update',
                                'put': 'update', 'delete': 'destroy'
                                }), name='message'),
    path('message-history/', MessageHistoryModelViewSet.as_view({'get': 'list'}), name='message_history'),
    path('delete-account/', delete_user, name='delete_account')
]