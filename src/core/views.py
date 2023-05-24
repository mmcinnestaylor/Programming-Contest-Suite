from django.shortcuts import render
from django.core.cache import cache

import requests as req

from announcements.models import Announcement
from contestadmin.models import Contest
from contestsuite.settings import CACHE_TIMEOUT, DOMJUDGE_URL, GUILD_ID
from register.models import Team
from manager.models import Course, Profile
from lfg.models import LFGProfile

# Create your views here.

# Display index page
def index(request):
    context = {}

    if cache.get('domjudge_status'):
        context['domjudge_status'] = cache.get('domjudge_status')
    else:
        try:
            r = req.head(DOMJUDGE_URL)
        except req.ConnectionError:
            context['domjudge_status'] = None
        else:
            context['domjudge_status'] = r.status_code
            cache.set('domjudge_status', r.status_code, CACHE_TIMEOUT)
    
    context['contest'] = cache.get_or_set(
        'contest_model', Contest.objects.first(), CACHE_TIMEOUT)
    
    context['announcements'] = (Announcement.objects.filter(status=1))
    context['courses'] = Course.objects.all()
    context['lfg_profiles_upper'] = LFGProfile.objects.filter(active=True).filter(division=1).count()
    context['lfg_profiles_lower'] = LFGProfile.objects.filter(active=True).filter(division=2).count()    
    context['guild_id'] = GUILD_ID

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

    # Aggregate upper division team and participant info
    upper_teams_set = teams_set.filter(division=1).filter(faculty=False).exclude(num_members=0)
    context['upper_teams'] = upper_teams_set.order_by('-questions_answered', 'score', 'name')
    context['num_upper_teams'] = upper_teams_set.count()
    context['num_upper_participants'] = participants_set.filter(team__division=1).count()

    #  Aggregate lower division team and participant info
    lower_teams_set = teams_set.filter(division=2).filter(faculty=False).exclude(num_members=0)
    context['lower_teams'] = lower_teams_set.order_by('-questions_answered', 'score', 'name')
    context['num_lower_teams'] = lower_teams_set.count()
    context['num_lower_participants'] = participants_set.filter(team__division=2).count()

    # Aggregate faculty team and participant info
    faculty_teams_set = teams_set.filter(faculty=True).exclude(num_members=0)
    context['faculty_teams'] = faculty_teams_set.order_by('-questions_answered', 'score', 'name')
    context['num_faculty_teams'] = faculty_teams_set.count()
    context['num_faculty_participants'] = participants_set.filter(team__faculty=True).count()

    return render(request, 'core/teams.html', context)
