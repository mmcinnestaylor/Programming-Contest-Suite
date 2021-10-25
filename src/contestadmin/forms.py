from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple

from contestadmin.models import Contest


class CheckinUsersForm(forms.Form):
    ACTION = (
        (1, 'Live Checkin'),
        (2, 'Practice Checkin'),
        (3, 'Checkout')
    )

    action = forms.ChoiceField(choices=ACTION)


class GenerateWalkinForm(forms.Form):
    DIVISION = (
        (1, 'Upper Division'),
        (2, 'Lower Division')
    )

    total = forms.IntegerField()
    division = forms.ChoiceField(choices=DIVISION)


class ResultsForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['results']
