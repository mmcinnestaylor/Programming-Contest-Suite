from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from . import forms

# Create your views here.


def checkin(request):
	context = {}

	if request.method == 'POST':
		email_form = forms.EmailCheckinForm(request.POST)
		swipe_form = forms.SwipeCheckinForm(request.POST)

		if email_form.is_valid() and swipe_form.is_valid():
			if email_form.cleaned_data['email']:
				try:
					user = User.objects.get(email=email_form.cleaned_data['email'])
					# user.profile.checked_in = True
					# user.save()

					messages.success(request, str(user.first_name) + ', you are checked in!', fail_silently=True)
				except:
					messages.error(request, 'Checkin failed', fail_silently=True)

				return redirect('checkin_result')
			elif swipe_form.cleaned_data['fsu_num']:
				if swipe_form.valid_read():
					# fsu_num = swipe_form.parse()
					fsu_num = swipe_form.cleaned_data['fsu_num']
					try:
						user = User.objects.get(profile__fsu_num=fsu_num)
						# user.profile.checked_in = True
						# user.save()

						messages.success(request, str(user.first_name) +
										', you are checked in!', fail_silently=True)
					except:
						messages.error(request, 'Checkin failed', fail_silently=True)

					return redirect('checkin_result')
				else:
					messages.error(request, 'Invalid card read', fail_silently=True)
	else:
		email_form = forms.EmailCheckinForm()
		swipe_form = forms.SwipeCheckinForm()

	context['email_form'] = email_form
	context['swipe_form'] = swipe_form
	return render(request, 'checkin/checkin.html', context)


def checkin_result(request):
	return render(request, 'checkin/checkin_result.html')

