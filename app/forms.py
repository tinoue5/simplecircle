from django import forms
from .models import Message,Circle

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={'rows':3,'cols':30})
        }

class CircleForm(forms.ModelForm):

    class Meta:
        model = Circle
        fields = ["name"]
