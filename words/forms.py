from django import forms
from .models import Word

class WordForm(forms.Form):
    word_name = forms.CharField(label='מילה', max_length=100)
    word_def = forms.CharField(label="הגדרה",max_length=200,widget=forms.Textarea)
    word_example = forms.CharField(label="דוגמא",max_length=200,widget=forms.Textarea)
    word_tags = forms.CharField(label='קטגוריות', max_length=100)

    class Meta:
        model = Word


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
