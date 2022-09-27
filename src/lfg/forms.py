from django import forms

from .models import LFGProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = LFGProfile
        fields = ('discord_username', 'discord_discriminator', 'division', 'standing')
        labels = {
            'discord_username': 'Discord Username', 
            'discord_discriminator': 'Discord Discriminator', 
            'division': 'Preferred Division', 
            'standing': 'Standing',
        }
        help_texts = {
            'discord_username': 'Your username before the #.', 
            'discord_discriminator': 'The number after the #.', 
            'division': 'The division in which you intend to compete.', 
        }
        error_messages = {
            'discord_username': {
                'max_length': "The username entered is too long.",
            },
            'discord_discriminator': {
                'max_length': "The discriminator entered is too long.",
            },
        }
