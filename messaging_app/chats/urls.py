from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .auth import RegisterViewset, CustomLoginView
from .views import ALLUserViewset, ConversationViewSet, MessageViewSet
from .custom_routers import NestedDefaultRouter

router = routers.DefaultRouter()
router.register(r'users', ALLUserViewset, basename='users')
# router = NestedDefaultRouter()
router.register(r'conversation', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterViewset.as_view(), name="signup"),
    path('login/', CustomLoginView.as_view(), name='login')
]

urlpatterns += router.urls
