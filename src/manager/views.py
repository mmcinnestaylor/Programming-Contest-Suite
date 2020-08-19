from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import transaction
#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . import forms
from .models import Profile
from register.models import Team 

# Create your views here.

@login_required
def base(request):
    context = {}
    context['courses'] = request.user.profile.courses.all()

    if not request.user.profile.has_team():
        messages.warning(
            request, 'You are not a member of a registered team. You must be a team member in order to compete. Check out the FAQ for more information.')
    if not request.user.profile.has_courses():
        messages.warning(
            request, 'You have not added any extra credit courses. You must add them to your profile in order to receive credit. Check out the FAQ for more information.')
    if request.user.profile.fsu_id is None or request.user.profile.fsu_id == '':
        messages.warning(
            request, 'Your FSU ID is blank. You must add it to your profile in order to receive extra credit. Check out the FAQ for more information.')
    if request.user.profile.fsu_num is None or request.user.profile.fsu_num == '':
        messages.info(
            request, 'Your FSU number is blank. You must add it to your profile in order to swipe check in on contest day. Check out the FAQ for more information.')

    return render(request, 'manager/manage.html', context)


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!', fail_silently=True)
            return redirect('manage_base')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)
    return render(request, 'manager/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
@transaction.atomic
def team(request):
    if request.user.profile.team_admin:
        if request.method == 'POST':
            form = forms.TeamForm(request.POST, instance=request.user.profile.team)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Your team was successfully updated!', fail_silently=True)
                return redirect('manage_base')
            else:
                messages.error(request, 'Please correct the error below.', fail_silently=True)
        else:
            form = forms.TeamForm(instance=request.user.profile.team)
        return render(request, 'manager/team_form.html', {'form': form})
    else:
        messages.info(
            request, 'You cannot manage a team because you are not a team admin', fail_silently=True)
        return redirect('manage_base')


@login_required
@transaction.atomic
def join_team(request):
    if not request.user.profile.has_team():
        if request.method == 'POST':
            form = forms.JoinForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['team'].num_members <= 2:
                    if form.cleaned_data['pin'] == form.cleaned_data['team'].pin:
                        request.user.profile.team = form.cleaned_data['team']
                        request.user.save()

                        request.user.profile.team.num_members += 1
                        member_name = request.user.get_full_name()
                        request.user.profile.team.members.append(member_name)
                        request.user.profile.team.save()

                        messages.success(
                            request, 'You have joined the team!', fail_silently=True)
                        return redirect('manage_base')
                    else:
                        messages.error(
                            request, 'The PIN you entered is incorrect. Please try again', fail_silently=True)
                else:
                    messages.error(
                        request, 'The team you have selected is full. Please select another team, or create your own.', fail_silently=True)
        else:
            form = forms.JoinForm()
        return render(request, 'manager/join_form.html', {'form': form})
    else:
        messages.info(
            request, 'You cannot join a new team before leaving or deleting (team admin only) your current team.', fail_silently=True)
        return redirect('manage_base')


@login_required
@transaction.atomic
def leave_team(request):
    if request.user.profile.has_team():
        if request.user.profile.team_admin:
            # If admin tries to leave a solo team, then just delete it
            if request.user.profile.team.num_members == 1:
                request.user.profile.team.delete()
                request.user.profile.team = None
                request.user.profile.team_admin = False
                request.user.save()

                messages.success(
                    request, 'You have left the team!', fail_silently=True)
                return redirect('manage_base')
            # If admin leaves a team with 2 or more people, then reassign admin credential first
            else: 
                messages.warning(
                    request, 'Not yet implemented', fail_silently=True)
                return redirect('manage_base')
        else:
            request.user.profile.team.num_members -= 1
            request.user.profile.team.members.remove(request.user.get_full_name())
            request.user.profile.team.save()

            request.user.profile.team = None
            request.user.save()

            messages.success(
                request, 'You have left the team!', fail_silently=True)
            return redirect('manage_base')
    else:
        messages.info(
            request, 'You cannot leave a team because you are not a team member.', fail_silently=True)
@login_required
@transaction.atomic
def delete_team(request):
    if request.user.profile.team_admin:
        request.user.profile.team.delete()
        request.user.profile.team = None
        request.user.profile.team_admin = False
        request.user.save()
  
        messages.success(
            request, 'You have deleted the team!', fail_silently=True)
        return redirect('manage_base')
    else:
        messages.info(
            request, 'You cannot delete a team because you are not a team admin.', fail_silently=True)
        return redirect('manage_base')

