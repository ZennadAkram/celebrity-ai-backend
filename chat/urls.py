from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from .views import UserViewSet, CelebrityViewSet, ChatSessionViewSet, MessageViewSet
from .views import CategoryViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'celebrities', CelebrityViewSet)
router.register(r'chats', ChatSessionViewSet)
router.register(r'messages', MessageViewSet)

router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # JWT authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    ]


