from django.shortcuts import redirect, render
from django.db import transaction
from django.http import HttpResponse
from django.contrib import messages

from . import forms

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return HttpResponse("You have already registered...") #add template
    else:
        return render(request, 'register/register.html')


def account(request):
    if request.user.is_authenticated:
        return HttpResponse("You have already registered, redirecting to Manage....") #add template
    else:
        if request.method == 'POST':
            form = forms.ExtendedUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        else:
            form = forms.ExtendedUserCreationForm()

    return render(request, 'register/account.html', {'form': form})