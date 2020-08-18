from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . import forms
from .models import Profile
from register.models import Team 

# Create your views here.

@login_required
def base(request):
    context = {}

    profile = Profile.objects.get(pk=request.user)
    courses = profile.courses.all()

    context['profile'] = profile
    context['courses'] = courses
    return render(request, 'manager/manage.html', context)
