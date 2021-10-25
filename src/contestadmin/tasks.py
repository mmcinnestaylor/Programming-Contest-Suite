import csv
import os

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from celery import shared_task
from celery.utils.log import get_task_logger

from contestsuite.settings import MEDIA_ROOT, DEFAULT_FROM_EMAIL
from contestadmin.models import Contest
from manager.models import Course, Faculty, Profile
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
        pin = User.objects.make_random_password(length=6)
        Team.objects.create(name=name, division=division, pin=pin)
        logger.info('Created walk-in team %d' % (i+1))

    logger.info('Walk-in team creation complete')


@shared_task
@transaction.atomic
def generate_contest_files():
    count = 0
    teams = Team.objects.all()

    logger.info('Starting team credential creation')

    for team in teams:
        count += 1
        team.contest_id = 'acm-' + str(count).zfill(3)
        team.contest_password = User.objects.make_random_password(length=6)
        team.save()

    logger.info('Created credentials for %d teams' % count)

    
    for division in Team.DIVISION:
        if division[0] == 1:
            account_file = MEDIA_ROOT + '/contest_files/accounts_upper.tsv'
            group_file = MEDIA_ROOT + '/contest_files/groups_upper.tsv'
            team_file = MEDIA_ROOT + '/contest_files/teams_upper.tsv'
        else:
            account_file = MEDIA_ROOT + '/contest_files/accounts_lower.tsv'
            group_file = MEDIA_ROOT + '/contest_files/groups_lower.tsv'
            team_file = MEDIA_ROOT + '/contest_files/teams_lower.tsv'

        with open(account_file, 'w', newline='') as account_tsv:
            with open(group_file, 'w', newline='') as group_tsv:
                with open(team_file, 'w', newline='') as team_tsv:
                    account_writer = csv.writer(
                        account_tsv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                    group_writer = csv.writer(
                        group_tsv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                    team_writer = csv.writer(
                        team_tsv, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

                    account_writer.writerow(['accounts', '1'])
                    group_writer.writerow(['File_Version', '1'])
                    # Upper Division Group -> 10
                    # Lower Division Group -> 11
                    group_writer.writerow([division[0]+9, division[1]])
                    team_writer.writerow(['File_Version', '2'])                    

                    teams = Team.objects.filter(division=division[0])
                    for team in teams:
                        account_writer.writerow([
                            'team', 
                            team.contest_id, 
                            team.contest_id, 
                            team.contest_password, 
                            int((team.contest_id).strip("acm-")),
                        ])

                        team_writer.writerow([
                            int((team.contest_id).strip("acm-")), 
                            '', 
                            team.division, 
                            team.name, 
                            'Florida State University', 
                            'FSU', 
                            'USA', 
                            '',
                        ])

    logger.info('Successfully generated contest files')


@shared_task
@transaction.atomic
def check_in_out_users(action):
    # Check-in
    if action == 1 or action == 2:
        users = User.objects.all()

        for user in users:

            if user.profile.team == None or user.profile.checked_in == True:
                continue

            user.profile.checked_in = True
            user.save()

            
            if action == 1:
                subject = 'Programming Contest DOMJudge Credentials'
                message = render_to_string(
                    'checkin/team_credentials_email.html', {'user': user})
            else:
                subject = 'Practice Contest DOMJudge Credentials'
                message = render_to_string(
                    'checkin/team_credentials_practice_email.html', {'user': user})
            user.email_user(subject, message)

            logger.info('Sent credentials to %s' % user.username)
    # Check-out
    else:
        users = User.objects.all()

        for user in users:
            user.profile.checked_in = False
            user.save()


@shared_task
def generate_ec_reports():
    num_courses = 0
    faculty_members = Faculty.objects.all()

    for faculty in faculty_members:
        courses = Course.objects.filter(instructor=faculty)
        num_files = 0

        for course in courses:
            students = User.objects.filter(profile__courses=course).filter(profile__checked_in=True)

            if students.exists():
                num_courses += 1
                num_files += 1
                filename = MEDIA_ROOT+'/ec_files/'+(faculty.email.split('@'))[0]+'_'+course.code+'.csv'

                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(
                        ['fsu_id', 'last_name', 'first_name', 'questions_answered', 'role'])
                    for student in students:
                        if student.profile.role == 1:
                            role = 'Contestant'
                        elif student.profile.role == 2:
                            role = 'Proctor'
                        elif student.profile.role == 3:
                            role = 'Question Writer'
                        else:
                            role = 'Organizer'

                        if student.profile.team is None:
                            questions_answered = 0
                        else:
                            questions_answered = student.profile.team.questions_answered

                        writer.writerow([
                            student.profile.fsu_id,
                            student.last_name,
                            student.first_name,
                            questions_answered,
                            role
                        ])
            else:
                continue
    
    logger.info(
        'Processed extra credit files for %d courses' % num_courses)


@ shared_task
def email_faculty(domain):
    faculty_members = Faculty.objects.all()
    fpath = MEDIA_ROOT + '/ec_files/'

    for faculty in faculty_members:
        for fname in os.listdir(fpath):
            uid=((faculty.email).split('@'))[0]
            if uid in fname: #not faculty_nanmer
                message = render_to_string('contestadmin/ec_available_email.html', {
                    'faculty': faculty,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(uid)),
                })
                
                send_mail(
                    'Programming Contest EC files',
                    message,
                    DEFAULT_FROM_EMAIL,
                    [faculty.email],
                    fail_silently = False,
                )

                break



@ shared_task
@ transaction.atomic
def process_contest_results():
    num_teams = 0
    contest = Contest.objects.all().first()

    with open(contest.results.path) as resultsfile:
        results = csv.reader(resultsfile, delimiter="\t", quotechar='"')
        for row in results:
            #if 'acm-' in row[0]:
            # Exclude header of file
            if 'results' not in row[0]:
                if int(row[0]) < 10:
                    id='acm-00'+row[0]
                elif int(row[0]) < 100:
                    id='acm-0'+row[0]
                else:
                    id='acm-'+row[0]

                try:
                    #team= Team.objects.get(contest_id=row[0])
                    team = Team.objects.get(contest_id=id)
                    team.questions_answered= row[3]
                    team.save()
                    num_teams += 1
                except:
                    logger.info('Could not process contest results for %s teams' % id)
            else:
                pass

    logger.info('Processed contest results for %d teams' % num_teams)
