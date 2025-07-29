from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False)\
                   .only('id', 'sender', 'content', 'timestamp')  # optimize fields

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False) 
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # ✅ custom manager

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:30]}"

    def get_all_replies(self):
        """Recursively fetch all nested replies"""
        all_replies = []

        children = self.replies.all().select_related('sender', 'receiver')

        for reply in children:
            all_replies.append(reply)
            all_replies.extend(reply.get_all_replies())  # recursive call

        return all_replies
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for Message ID {self.message.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message {self.message.id}"
