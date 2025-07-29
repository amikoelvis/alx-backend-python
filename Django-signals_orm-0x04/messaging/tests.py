from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification

class MessagingSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        notification = Notification.objects.get(message=msg)
        self.assertEqual(notification.user, self.receiver)
        self.assertFalse(notification.is_read)

class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Original message')

    def test_message_edit_logs_history(self):
        self.message.content = 'Edited message'
        self.message.save()
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, 'Original message')
        self.assertTrue(self.message.edited)

class UserDeletionSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.msg = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hi!')
        self.note = Notification.objects.create(user=self.user2, message=self.msg)
        self.history = MessageHistory.objects.create(message=self.msg, old_content='Hi!', edited_by=self.user1)

    def test_user_deletion_cleans_data(self):
        self.user1.delete()
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.user1).exists())
