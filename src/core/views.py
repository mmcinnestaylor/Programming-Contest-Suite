from django.shortcuts import render

import requests as req


from announcements.models import Announcement
from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT, DOMJUDGE_URL
from register.models import Team
from manager.models import Course, Profile

# Create your views here.

# Display index page
def index(request):
    context = {}

    try:
        r = req.get(DOMJUDGE_URL)
    except:
        context['domjudge_status'] = None
    else:
        context['domjudge_status'] = r.status_code

    context['cache_timeout'] = CACHE_TIMEOUT
    try:
        context['contest'] = Contest.objects.first()
    except:
        context['contest'] = None
    
    context['announcements'] = (Announcement.objects.filter(status=1))
    context['courses'] = Course.objects.all()    

    return render(request, 'core/index.html', context)


# Display contact us page
def contact(request):
    return render(request, 'core/contact.html')


# Display faq page
def faq(request):
    return render(request, 'core/faq.html')


# Display teams page
def teams(request):
    context = {}

    teams_set = Team.objects.all()
    participants_set = Profile.objects.all()

    context['cache_timeout'] = CACHE_TIMEOUT

    # Aggregate upper division team and participant info
    upper_teams_set = teams_set.filter(division=1)
    context['upper_teams'] = upper_teams_set
    context['num_upper_teams'] = upper_teams_set.count()
    context['num_upper_participants'] = participants_set.filter(team__division=1).count()

    #  Aggregate division team and participant info
    lower_teams_set = teams_set.filter(division=2)
    context['lower_teams'] = lower_teams_set
    context['num_lower_teams'] = lower_teams_set.count()
    context['num_lower_participants'] = participants_set.filter(team__division=2).count()

    return render(request, 'core/teams.html', context)
