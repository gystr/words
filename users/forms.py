from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


class SignupForm(UserCreationForm):
    email = forms.EmailField(label=("אימייל"),max_length=200, help_text='Required')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
