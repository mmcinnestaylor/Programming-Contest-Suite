from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.core.mail import send_mail
from celery import shared_task

from register.models import Team


@shared_task
def create_walkin_teams():
    pass


@shared_task
def generate_team_credentials():
    count = 1
    teams =  Team.objects.all()

    for team in teams:
        team.contest_id = 'acm-' + str(count).zfill(3)
        team.contest_password = User.objects.make_random_password(length=6)
        team.save()
        count+=1
