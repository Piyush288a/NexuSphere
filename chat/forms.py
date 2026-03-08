from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message_text', 'file_attachment']
        widgets = {
            'message_text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Type your message here...',
                'rows': 3
            }),
            'file_attachment': forms.FileInput(attrs={
                'class': 'form-file'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message_text'].label = 'Message'
        self.fields['file_attachment'].label = 'Attachment (optional)'
        self.fields['file_attachment'].required = False
