import csv

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction

from celery import shared_task
from celery.utils.log import get_task_logger

from contestsuite.settings import MEDIA_ROOT
from contestadmin.models import Contest
from manager.models import Course, Faculty
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


@shared_task
@transaction.atomic
def process_contest_results():
    total = 0
    contest = Contest.objects.all().first()

    with open(contest.results.path) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            if 'acm-' in row[0]:
                team = Team.objects.get(contest_id=row[0])
                team.questions_answered = row[3]
                team.save()
                total += 1
            else:
                pass
        
        logger.info('Processed contest results for %d teams' % total)


@shared_task
def generate_domjudge_files():
    #teams = Team.objects.all()

    filename = MEDIA_ROOT +'/contest_files/groups.tsv'

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['File_Version', '1'])
        for division in Team.DIVISION:
            writer.writerow([division[0], division[1]])


@shared_task
def generate_ec_forms():
    total = 0
    faculty_members = Faculty.objects.all()

    for faculty in faculty_members:
        courses = Course.objects.filter(instructor=faculty)

        for course in courses:
            students = User.objects.filter(profile__checked_in=True).filter(profile__courses=course)
            filename = 'media/ec_files/'+faculty.last_name+'-'+(faculty.first_name)[0]+'-'+course.code+'.csv'
            
            with open(filename,'w', newline='') as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['fsu_id', 'last_name', 'first_name', 'questions_answered'])
                for student in students:
                    writer.writerow([student.profile.fsu_id, student.last_name, student.first_name, student.profile.team.questions_answered])
            
            total += 1
    
    logger.info(logger.info('Processed extra credit files for %d courses' % total))
