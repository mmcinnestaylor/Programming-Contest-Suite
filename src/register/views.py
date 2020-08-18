from django.shortcuts import redirect, render
from django.db import transaction
# from django.http import HttpResponse
# from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from . import forms
from . import models
from manager.models import Profile

# Create your views here.

def base(request):
    if request.user.is_authenticated:
        return redirect('manage_base')
    return render(request, 'register/register.html')


@transaction.atomic
def account(request):
    if request.user.is_authenticated:
        return redirect('manage_base')
    else:
        if request.method == 'POST':
            form = forms.ExtendedUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = forms.ExtendedUserCreationForm()
        return render(request, 'register/register_form.html', {'page_title': 'Contest Registration', 'heading' : 'Contest', 'form': form})


@login_required
@transaction.atomic
def team(request):
    if request.user.profile.has_team():
        return redirect('manage_base')
    else:
        if request.method == 'POST':
            form = forms.TeamForm(request.POST)
            if form.is_valid():
                newTeam = form.save(commit=False)
                newTeam.password = User.objects.make_random_password(length=10)
                newTeam.pin = User.objects.make_random_password(length=4)
                memberName = request.user.get_full_name()
                newTeam.members.append(memberName)
                newTeam.save()

                request.user.profile.team = newTeam
                request.user.profile.team_admin = True
                request.user.profile.save()
                
                return redirect('manage_base')
        else:
            form = forms.TeamForm()
        return render(request, 'register/register_form.html', {'page_title': 'Team Registration', 'heading': 'Team', 'form': form})
