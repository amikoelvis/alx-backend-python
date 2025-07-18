from django.contrib import admin
from django.urls import path, include   # include is required for nested routes

urlpatterns = [
    path('admin/', admin.site.urls),

    #  All API endpoints from the chats app will now live under /api/
    path('api/', include('chats.urls')),
]

# always explicitly include from django.urls import path, include