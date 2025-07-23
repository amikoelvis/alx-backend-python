from django.contrib import admin
from django.urls import path, include  # include is required
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # Corrected import

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL

    # All chats API endpoints now live under /api/
    path('api/', include('chats.urls')),  # Includes your app's URL patterns

    # Add DRF's browsable API login/logout
    path('api-auth/', include('rest_framework.urls')),  # For DRF's browsable API (authentication views)

    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtain JWT access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh JWT token
]
