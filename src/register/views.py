from django.shortcuts import redirect, render
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.forms import formset_factory

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


# key error on password1, more research required
# https://stackoverflow.com/questions/34962398/keyerror-at-registration-value-password1/34963664

'''def group(request):
    context = {}
    UserFormSet = formset_factory(forms.ExtendedUserCreationForm, extra=3)
    
    if request.method == 'POST':
        formset = UserFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    new_user = User(
                        first_name=form.cleaned_data['first_name'], 
                        last_name=form.cleaned_data['last_name'],
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password1']
                    )
                    # new_user = form.save(commit=False)
                    # new_user.password = form.cleaned_data['password1']
                    new_user.save()
            
            messages.success(
                request, 'Accounts registered!')
            return redirect('index')
        
        messages.error(
            request, 'Please correct the error(s) below.', fail_silently=True)
    else:
        formset = UserFormSet()

    context['formset'] = formset
    return render(request, 'register/group_register_form.html', {'formset': formset})'''


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
