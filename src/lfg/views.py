from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test

from . import forms, tasks
from .models import LFGProfile
from .utils import profile_activatable, new_lfg_user, lfg_profile_active, current_lfg_user

# Create your views here.

@login_required
def dashboard(request):
    context = {}

    context['standings'] = {standing[0]:standing[1] for standing in LFGProfile.STANDING}#['Graduate', 'Senior', 'Junior', 'Sophomore', 'Freshman', 'Other']
    context['divisions'] = {division[0]:division[1] for division in LFGProfile.DIVISION}
    context['lfg_upper'] = LFGProfile.objects.filter(active=True).filter(division=1)
    context['lfg_lower'] = LFGProfile.objects.filter(active=True).filter(division=2)

    return render(request, 'lfg/dashboard.html', context)


@login_required
@user_passes_test(profile_activatable, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def activate_profile(request):
    request.user.lfgprofile.active = True
    request.user.lfgprofile.save()

    #tasks.add_lfg_role.delay(request.user.lfgprofile.get_discord_username(), request.user.lfgprofile.division)
    tasks.manage_discord_lfg_role.delay(request.user.lfgprofile.get_discord_username(), request.user.lfgprofile.division, 'add')
    messages.success(request, 'Profile scheduled for activation.', fail_silently=True)
    
    return redirect('lfg_dashboard')


@login_required
@user_passes_test(new_lfg_user, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def create_profile(request):
    context = {}

    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST)
        
        if profile_form.is_valid():
            lfg_profile = profile_form.save(commit=False)
            lfg_profile.completed = lfg_profile.is_completed()
            lfg_profile.user=request.user
            lfg_profile.save()

            messages.success(request, 'Your profile was created.', fail_silently=True)

            return redirect('lfg_dashboard')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        profile_form = forms.ProfileForm()

    context['profile_form'] = profile_form

    return render(request, 'lfg/profile_form.html', context)


@login_required
@user_passes_test(lfg_profile_active, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def deactivate_profile(request):
    request.user.lfgprofile.active = False
    request.user.lfgprofile.save()

    #tasks.remove_lfg_role.delay(request.user.lfgprofile.get_discord_username(), request.user.lfgprofile.division)
    tasks.manage_discord_lfg_role.delay(request.user.lfgprofile.get_discord_username(), request.user.lfgprofile.division, 'remove')
    messages.warning(request, 'Profile scheduled for deactivation.', fail_silently=True)

    return redirect('lfg_dashboard')


@login_required
@user_passes_test(current_lfg_user, login_url='/lfg/', redirect_field_name=None)
@transaction.atomic
def manage_profile(request):
    context = {}

    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, instance=request.user.lfgprofile)

        if profile_form.is_valid():
            lfg_profile = profile_form.save(commit=False)

            # Username change
            if 'discord_username' in profile_form.changed_data or 'discord_discriminator' in profile_form.changed_data:
                if lfg_profile.verified:
                    lfg_profile.verified = False
                if lfg_profile.active:
                    lfg_profile.active = False
                    username = profile_form['discord_username'].initial+'#'+str(profile_form['discord_discriminator'].initial)

                    if 'division' not in profile_form.changed_data:
                        #tasks.remove_lfg_role.delay(username, lfg_profile.division)
                        tasks.manage_discord_lfg_role.delay(username, lfg_profile.division, 'remove')
                    else:
                        #tasks.remove_lfg_role.delay(username, profile_form['division'].initial)
                        tasks.manage_discord_lfg_role.delay(username, profile_form['division'].initial, 'remove')

                messages.warning(request, 'Discord username changed. Profile reverification required.', fail_silently=True)
            # Username unchanged
            else:
                # Division was updated 
                if 'division' in profile_form.changed_data:
                    if lfg_profile.active: 
                        if profile_form.cleaned_data['division'] is not None:
                            #tasks.change_lfg_role.delay(lfg_profile.get_discord_username(), profile_form['division'].initial)
                            tasks.manage_discord_lfg_role.delay(lfg_profile.get_discord_username(), profile_form['division'].initial, 'swap')
                        else:
                            lfg_profile.active = False

                            #tasks.remove_lfg_role.delay(lfg_profile.get_discord_username(), profile_form['division'].initial)
                            tasks.manage_discord_lfg_role.delay(lfg_profile.get_discord_username(), profile_form['division'].initial, 'remove')
                            messages.warning(request, 'Profile deactivated because it is incomplete. Complete the blank field(s)  to reactivate.', fail_silently=True)
                elif 'standing' in profile_form.changed_data and lfg_profile.active:
                    if profile_form.cleaned_data['standing'] is None:
                        #tasks.remove_lfg_role.delay(lfg_profile.get_discord_username(), profile_form['standing'].initial)
                        tasks.manage_discord_lfg_role.delay(lfg_profile.get_discord_username(), profile_form['division'].initial, 'remove')
                        messages.warning(request, 'Profile deactivated because it is incomplete. Complete the blank field(s)  to reactivate.', fail_silently=True)

            lfg_profile.completed = lfg_profile.is_completed()
            lfg_profile.save()
            
            return redirect('lfg_dashboard')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        profile_form = forms.ProfileForm(instance=request.user.lfgprofile)

    context['profile_form'] = profile_form

    return render(request, 'lfg/profile_form.html', context)
