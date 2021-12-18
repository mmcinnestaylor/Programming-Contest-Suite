from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect

from . import forms
from . import tasks
from register.models import Team

# Create your views here.


@staff_member_required
@transaction.atomic
def checkin(request):
	context = {}

	if request.method == 'POST':
		email_form = forms.EmailCheckinForm(request.POST)
		swipe_form = forms.SwipeCheckinForm(request.POST)
		walkin_form = forms.WalkinForm(request.POST)
		walk_in_team = None
		is_walkin = False

		if email_form.is_valid() and swipe_form.is_valid() and walkin_form.is_valid():
			# Process a walk-in selection, if one is made.
			if walkin_form.cleaned_data['division']:
				# Get team from selected division
				if walkin_form.cleaned_data['division'] == '1':
					walk_in_team = Team.objects.filter(name__contains='Walk-in-U-').filter(num_members=0).first()						
				else:
					walk_in_team = Team.objects.filter(name__contains='Walk-in-L-').filter(num_members=0).first()
				
				# If an empty walkin-is is not found, notify user.
				if walk_in_team is None:
					messages.error(request, 'There are no Walk-in teams available.', fail_silently=True)
					return redirect('checkin_result')
				
				is_walkin = True

			# Process email form entry, if it has been made.
			if swipe_form.cleaned_data['fsu_num']:
				if swipe_form.valid_read():
					fsu_number = swipe_form.parse()

					try:
						user = User.objects.get(profile__fsu_num=fsu_number)
					except:
						messages.error(
							request, 'Check in failed. FSU number not found.', fail_silently=True)
					else:
						if user.profile.checked_in:
							messages.info(request, 'You are already checked in.',
							              fail_silently=True)
						elif user.profile.team is None and not is_walkin:
							messages.info(
								request, 'You are not a member of a registered team. Join a registered team, or select YES at the walk-in prompt.', fail_silently=True)
						else:
							user.profile.checked_in = True
							if is_walkin == True:
								if user.profile.has_team():
									messages.info(
										request, 'You are a member of a registered team. Walk-in selection ignored.', fail_silently=True)
								else:
									# update user
									user.profile.team = walk_in_team

									#update team
									walk_in_team.num_members += 1
									walk_in_team.save()

							user.save()

							# Email user DOMjudge credentials
							tasks.send_credentials.delay(user.username)
							messages.success(request, str(user.first_name) +
							                 ', you are checked in!', fail_silently=True)
							messages.info(
								request, 'Check your registered email or account dashboard for DOMJudge credentials.', fail_silently=True)
				else:
					messages.error(
						request, 'Invalid card read. Please try again.', fail_silently=True)

			# Process email form entry, if it has been made.
			elif email_form.cleaned_data['email']:
				try:
					user = User.objects.get(email=email_form.cleaned_data['email'])
				except:
					messages.error(
						request, 'Check in failed. Email address not found.', fail_silently=True)
				else:
					if user.profile.checked_in:
						messages.info(request, 'You are already checked in.', fail_silently=True)
					elif user.profile.team is None and not is_walkin:
						messages.info(request, 'You are not a member of a registered team. Join a registered team, or select YES at the walk-in prompt.', fail_silently=True)
					else:
						user.profile.checked_in = True
						if is_walkin == True:
							if user.profile.has_team():
								messages.info(request, 'You are a member of a registered team. Walk-in selection ignored.', fail_silently=True)
							else:
								# update user
								user.profile.team = walk_in_team

								#update team
								walk_in_team.num_members += 1
								walk_in_team.save()

						user.save()

						# Email user DOMjudge credentials
						tasks.send_credentials.delay(user.username)
						messages.success(request, str(user.first_name) + ', you are checked in!', fail_silently=True)
						messages.info(request, 'Check your registered email or account dashboard for DOMJudge credentials.', fail_silently=True)
			
			else:
				messages.error(request, 'Invalid form submission. Please resubmit your information.', fail_silently=True)

			return redirect('checkin_result')

	else:
		email_form = forms.EmailCheckinForm()
		swipe_form = forms.SwipeCheckinForm()
		walkin_form = forms.WalkinForm()

	context['email_form'] = email_form
	context['swipe_form'] = swipe_form
	context['walkin_form'] = walkin_form
	return render(request, 'checkin/checkin.html', context)


@staff_member_required
def checkin_result(request):
	return render(request, 'checkin/checkin_result.html')
