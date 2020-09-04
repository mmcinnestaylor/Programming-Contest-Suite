from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction

from celery import shared_task
from celery.utils.log import get_task_logger

from register.models import Team


logger = get_task_logger(__name__)


@shared_task
@transaction.atomic
def create_walkin_teams(**kwargs):
    logger.info('Starting walk-in team creation')

    for i in range(kwargs['total']):
        if kwargs['division'] == 1:
            name = 'Walk-in-U-' + str(i+1).zfill(3)
        else:
            name = 'Walk-in-L-' + str(i+1).zfill(3)
        pin = User.objects.make_random_password(length=4)
        Team.objects.create(name=name, division=kwargs['division'], pin=pin)
        logger.info('Created walk-in team %d' % (i+1))


@shared_task
@transaction.atomic
def generate_team_credentials():
    count = 1
    teams =  Team.objects.all()

    logger.info('Starting team credential creation')

    for team in teams:
        team.contest_id = 'acm-' + str(count).zfill(3)
        team.contest_password = User.objects.make_random_password(length=6)
        team.save()
        count+=1
        logger.info('Created credentials for %s' % team.contest_id)
