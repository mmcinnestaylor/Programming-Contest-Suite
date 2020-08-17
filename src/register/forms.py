from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Team

# Extend built-in User form to include email, first name, and last name fields
class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # name lengths as specified by Django 3.0.* documentation
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'division']
        help_texts = {
            'name': '30 characters max. Keep it PG-13 please!',
            'division': 'The division in which your team will compete.',
        }
        error_messages = {
            'name': {
                'max_length': "This team name is too long.",
            },
        }