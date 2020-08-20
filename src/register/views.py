from django.shortcuts import redirect, render
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from . import forms
from . import models
from manager.utils import has_no_team, not_registered

# Create your views here.

def base(request):
    return render(request, 'register/register.html')


# Limit view to those who are not logged in. Others redirected to manage.
@user_passes_test(not_registered, login_url='/manage/')
@transaction.atomic
def account(request):
    if request.method == 'POST':
        form = forms.ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Account registered!')
            return redirect('login')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        form = forms.ExtendedUserCreationForm()
    return render(request, 'register/register_form.html', {'page_title': 'Contest Registration', 'heading' : 'Contest', 'form': form})


# Limit view to those are not on a team. Others redirected to manage.
@login_required
@user_passes_test(has_no_team, login_url='/manage/')
@transaction.atomic
def team(request):
    if request.method == 'POST':
        form = forms.TeamForm(request.POST)
        if form.is_valid():
            # Create a temporary object, add additional attribute data, then save to DB
            newTeam = form.save(commit=False)
            newTeam.pin = User.objects.make_random_password(length=4)
            memberName = request.user.get_full_name()
            newTeam.members.append(memberName)
            newTeam.save()

            # Update user profile with new team
            request.user.profile.team = newTeam
            request.user.profile.team_admin = True
            request.user.profile.save()
            
            messages.success(
                request, 'Team registered!', fail_silently=True)
            return redirect('manage_base')

        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        form = forms.TeamForm()
    return render(request, 'register/register_form.html', {'page_title': 'Team Registration', 'heading': 'Team', 'form': form})
