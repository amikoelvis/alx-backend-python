from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Prefetch
from messaging.models import Message
from messaging.forms import MessageForm

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
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')  # or wherever
    else:
        form = MessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})
