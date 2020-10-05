import csv

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


from celery import shared_task
from celery.utils.log import get_task_logger

from contestsuite.settings import MEDIA_ROOT, DEFAULT_FROM_EMAIL
from contestadmin.models import Contest
from manager.models import Course, Faculty
from register.models import Team


logger = get_task_logger(__name__)


@shared_task
@transaction.atomic
def create_walkin_teams(division, total):
    logger.info('Starting walk-in team creation')

    if division == 1:
        base_name = 'Walk-in-U-'
        existing_count = Team.objects.filter(
            name__contains='Walk-in-U-').count()
    else:
        base_name = 'Walk-in-L-'
        existing_count = Team.objects.filter(
            name__contains='Walk-in-L-').count()

    for i in range(total):
        '''if division == 1:
            name = 'Walk-in-U-' + str(upper_count+i+1).zfill(3)
        else:
            name = 'Walk-in-L-' + str(lower_count+i+1).zfill(3)'''
        name = base_name + str(existing_count+i+1).zfill(3)
        pin = User.objects.make_random_password(length=4)
        Team.objects.create(name=name, division=division, pin=pin)
        logger.info('Created walk-in team %d' % (i+1))


@shared_task
@transaction.atomic
def generate_contest_files():
    count = 1
    teams = Team.objects.all()

    logger.info('Starting team credential creation')

    for team in teams:
        team.contest_id = 'acm-' + str(count).zfill(3)
        team.contest_password = User.objects.make_random_password(length=6)
        team.save()
        count += 1
        logger.info('Created credentials for %s' % team.contest_id)

    group_file = MEDIA_ROOT + '/contest_files/groups.tsv'
    with open(group_file, 'w', newline='') as group_tsv:
        writer = csv.writer(group_tsv, delimiter='\t',
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['File_Version', '1'])
        for division in Team.DIVISION:
            writer.writerow([division[0], division[1]])

    account_file = MEDIA_ROOT + '/contest_files/accounts.tsv'
    team_file = MEDIA_ROOT + '/contest_files/teams.tsv'
    with open(account_file, 'w', newline='') as account_tsv:
        with open(team_file, 'w', newline='') as team_tsv:
            account_writer = csv.writer(
                account_tsv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            team_writer = csv.writer(
                team_tsv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

            account_writer.writerow(['accounts', '1'])
            team_writer.writerow(['File_Version', '2'])

            for team in teams:
                account_writer.writerow([
                    'team',
                    team.contest_id,
                    team.contest_id,
                    team.contest_password],
                    int((team.contest_id).strip("acm-"))
                ])

                team_writer.writerow([
                    int((team.contest_id).strip("acm-")),
                    '',
                    team.division,
                    team.name,
                    'Florida State University',
                    'FSU',
                    'USA',
                    ''
                ])



@ shared_task
@ transaction.atomic
def process_contest_results():
    total= 0
    contest= Contest.objects.all().first()

    with open(contest.results.path) as fd:
        rd= csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            if 'acm-' in row[0]:
                team= Team.objects.get(contest_id=row[0])
                team.questions_answered= row[3]
                team.save()
                total += 1
            else:
                pass

        logger.info('Processed contest results for %d teams' % total)


@ shared_task
def generate_ec_forms(domain):
    total = 0
    faculty_members = Faculty.objects.all()

    for faculty in faculty_members:
        courses = Course.objects.filter(instructor=faculty)

        for course in courses:
            students = User.objects.filter(profile__courses=course).filter(profile__checked_in=True)
            filename = 'media/ec_files/'+course.code+'-'+(faculty.email.split('@'))[0]+'.csv'

            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    ['fsu_id', 'last_name', 'first_name', 'questions_answered'])
                for student in students:
                    writer.writerow([student.profile.fsu_id, student.last_name,
                                    student.first_name, student.profile.team.questions_answered])

            total += 1

        message = render_to_string('contestadmin/ec_available_email.html', {
            'faculty': faculty,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(((faculty.email).split('@'))[0])),
        })
        
        send_mail(
            'Programming Contest EC files',
            message,
            DEFAULT_FROM_EMAIL,
            [faculty.email],
            fail_silently = False,
        )

    logger.info(logger.info(
        'Processed extra credit files for %d courses' % total))
