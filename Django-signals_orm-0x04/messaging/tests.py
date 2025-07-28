from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory

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
