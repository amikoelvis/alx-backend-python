from django import forms
from messaging.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content', 'parent_message']
