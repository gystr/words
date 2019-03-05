from django import forms
from .models import Word
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WordForm(forms.Form):
    word_name = forms.CharField(label='מילה', max_length=100)
    word_def = forms.CharField(label="הגדרה",max_length=200,widget=forms.Textarea)
    word_example = forms.CharField(label="דוגמא",max_length=200,widget=forms.Textarea)
    word_tags = forms.CharField(label='קטגוריות', max_length=100)

    class Meta:
        model = Word


class ContactForm(forms.Form):
    from_email = forms.EmailField(label='מייל',
    required=True,widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))

    subject = forms.CharField(label='נושא',
    required=True,widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))

    message = forms.CharField(label='תוכן',
    widget=forms.Textarea(attrs={'class' : 'myfieldclass'}), required=True)



class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
