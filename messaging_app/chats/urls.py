from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create DRF router
router = DefaultRouter()

# Register endpoints
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Export urlpatterns
urlpatterns = router.urls
