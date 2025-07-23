from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Conversation, Message

# Custom UserAdmin for the custom User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff')
        }),
    )
    filter_horizontal = ('groups', 'user_permissions')


# Registering the custom User model
admin.site.register(User, CustomUserAdmin)

# Conversation Model Admin
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    search_fields = ('conversation_id',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(Conversation, ConversationAdmin)


# Message Model Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'message_body', 'sent_at', 'is_read')
    search_fields = ('message_id', 'message_body__email', 'conversation__conversation_id')
    list_filter = ('sent_at', 'is_read')
    ordering = ('-sent_at',)

admin.site.register(Message, MessageAdmin)
