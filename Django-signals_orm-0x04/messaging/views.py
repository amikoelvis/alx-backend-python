from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Prefetch
from messaging.models import Message
from django.views.decorators.cache import cache_page 

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # Or a goodbye/feedback page

def get_conversation(user):
    return Message.objects.filter(receiver=user, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )

@login_required
def send_dummy_message(request):
    if request.method == 'POST':
        receiver = User.objects.first()
        message = Message.objects.create(
            sender=request.user, 
            receiver=receiver,
            content="Hello!",
        )
        return redirect('inbox')  # or anywhere

@cache_page(60)  # ✅ Cache this view for 60 seconds
@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})
