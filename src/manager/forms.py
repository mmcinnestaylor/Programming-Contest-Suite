from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError


from .models import Profile, Course
from register.models import Team


class UserForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check if email address is attached to an existing user
        if User.objects.filter(email=email).exists():
            try:
                user = User.objects.get(email=email)
            except:
                raise ValidationError('Unable to validate email.')
            else:
                # Email address associated with another account
                if user.username != self.user.username:
                    raise ValidationError('Email already in use.')
                # Email address associated with user's account    
                else:
                    return email
        return email
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        help_texts = {
            'first_name': '30 Characters max',
            'last_name': '150 Characters max',
            'email': 'Does NOT need to be your FSU email',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fsu_id', 'fsu_num')
        labels = {
            'fsu_id': 'FSU ID',
            'fsu_num': 'FSU number',
        }
        help_texts = {
            'fsu_id': 'Excluding @my.fsu.edu ex: ab12c@my.fsu.edu -> ab12c',
            'fsu_num': 'Last 8 numbers on FSUCard. Exclude spaces.',
        }
        error_messages = {
            'fsu_id': {
                'max_length': "The id entered is too long.",
            },
            'fsu_num': {
                'max_length': "The number entered is too long.",
            },
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('courses',)
        widgets = {'courses': forms.CheckboxSelectMultiple()}
        help_texts = {
            'courses': 'Select any course above in which you are currently registered.',
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'division')
        help_texts = {
            'name': '30 characters max. Keep it PG-13 please!',
            'division': 'The division in which your team will compete.',
        }


class JoinForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(
    ), label='Registered Teams', help_text='Teamname : Division where UPPER = 1 and LOWER = 2')
    pin = forms.CharField(
        max_length=6, label='PIN', help_text='Ask team admin for PIN')

