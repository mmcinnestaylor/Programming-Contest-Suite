from django.shortcuts import render
from register.models import Team
from manager.models import Profile

# Create your views here.


def index(request):
    return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def faq(request):
    return render(request, 'core/faq.html')


def teams(request):
    context = {}

    teams_set = Team.objects.all()
    participants_set = Profile.objects.all()

    upper_teams_set = teams_set.filter(division=2)
    context['upper_teams'] = upper_teams_set

    num_upper_teams = upper_teams_set.count()
    context['num_upper_teams'] = num_upper_teams

    num_upper_participants = participants_set.filter(team__division=2).count()
    context['num_upper_participants'] = num_upper_participants

    lower_teams_set = teams_set.filter(division=1)
    context['lower_teams'] = lower_teams_set

    num_lower_teams = lower_teams_set.count()
    context['num_lower_teams'] = num_lower_teams

    num_lower_participants = participants_set.filter(team__division=1).count()
    context['num_lower_participants'] = num_lower_participants

    return render(request, 'core/teams.html', context)
