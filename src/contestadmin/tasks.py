import csv
import os
from math import ceil, log10

from discord import Webhook, RequestsWebhookAdapter, InvalidArgument

from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from celery import shared_task
from celery.utils.log import get_task_logger

from contestsuite.settings import MEDIA_ROOT, DEFAULT_FROM_EMAIL, BOT_CHANNEL_WEBHOOK_URL
from contestadmin.models import Contest
from manager.models import Course, Faculty, Profile
from register.models import Team


logger = get_task_logger(__name__)


@shared_task
@transaction.atomic
def create_walkin_teams(division, total):
    if total > 0:
        logger.debug('Starting walk-in team creation')

        if division == 1:
            base_name = 'Walk-in-U-'
        else:
            base_name = 'Walk-in-L-'

        existing_teams = Team.objects.filter(
            name__contains=base_name)

        if existing_teams.exists():
            existing_count = existing_teams.count()
            existing_count_width = ceil(log10(existing_count))
            new_count_width = ceil(log10(existing_count+total))

            # Update existing team names if 0-padding width changes
            if new_count_width > existing_count_width:
                for team in existing_teams:
                    walkin_id = int(team.name.split("-")[-1])
                    team.name = f"{base_name}{str(walkin_id).zfill(new_count_width)}"
                    team.save()

                logger.debug("Renamed existing Walk-in teams.")
        else:
            existing_count = 0
            new_count_width = ceil(log10(total))

        # Create and write teams to db
        for i in range(1, total+1):
            name = f"{base_name}{str(existing_count+i).zfill(new_count_width)}"
            pin = User.objects.make_random_password(length=6)
            Team.objects.create(name=name, division=division, pin=pin)
            logger.debug(f'Created walk-in team {existing_count+i}')

        logger.info(f'{total} {base_name[:-1]} teams created.')
    else:
        logger.error("New Walk-in team count LEQ 0.")

@shared_task
@transaction.atomic
def generate_contest_files():
    count = 0
    teams = Team.objects.all()

    try:
        fill_width = ceil(log10(teams.count()))
    except:
        logger.error("Encountered invalid Team count.")
    else:
        logger.debug('Starting team credential creation')

        for team in teams:
            count += 1
            team.contest_id = 'acm-' + str(count).zfill(fill_width)
            team.contest_password = User.objects.make_random_password(length=6)
            team.save()

        logger.info(f'Created credentials for {count} teams')

        # Create DOMjudge contest files per division
        # https://www.domjudge.org/docs/manual/7.3/import.html
        for division in Team.DIVISION:
            if division[0] == 1:  # Upper
                account_file = MEDIA_ROOT + '/contest_files/accounts_upper.tsv'
                group_file = MEDIA_ROOT + '/contest_files/groups_upper.tsv'
                team_file = MEDIA_ROOT + '/contest_files/teams_upper.tsv'
            else:  # Lower
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

                        # File headers
                        account_writer.writerow(['accounts', '1'])
                        group_writer.writerow(['File_Version', '1'])
                        team_writer.writerow(['File_Version', '2'])

                        # Group info
                        # Upper Division Group -> 6
                        # Lower Division Group -> 7
                        group_writer.writerow([
                            division[0]+5,  # Category ID (int)
                            division[1]  # Name of the team category (str)
                        ])

                        # Write teams info for current division
                        teams = Team.objects.filter(division=division[0])
                        for team in teams:
                            # Account info
                            account_writer.writerow([
                                'team',  # User type (str): 'team' or 'judge'
                                team.contest_id,  # Full name of the user (str)
                                team.contest_id,  # DOMjudge Username (str)
                                team.contest_password,  # DOMjudge Password (str)
                                int((team.contest_id).strip("acm-")),
                            ])
                            # Team profile
                            team_writer.writerow([
                                int((team.contest_id).strip("acm-")), # Team Number (int)
                                '', # External ID (int) ** not used in our config **
                                team.division + 5, # Group ID (int)
                                team.name, # Team name (str)
                                'Florida State University', # Institution name (str)
                                'FSU', # Institution short name (str)
                                'USA', # Country code in ISO 3166-1 alpha-3 format
                                '', # external institution ID ** not used in our config **
                            ])

        logger.debug('Successfully generated contest files')


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
                subject = 'Programming Contest DOMjudge Credentials'
                message = render_to_string(
                    'checkin/team_credentials_email.html', {'user': user})
            else:
                subject = 'Practice Contest DOMjudge Credentials'
                message = render_to_string(
                    'checkin/team_credentials_practice_email.html', {'user': user})
            user.email_user(subject, message)

            logger.debug(f'Sent credentials to {user.username}')
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
        # All courses for given faculty member
        courses = Course.objects.filter(instructor=faculty)
        num_files = 0

        for course in courses:
            # All students in given course
            students = User.objects.filter(profile__courses=course).filter(profile__checked_in=True)

            if students.exists():
                num_courses += 1
                num_files += 1
                filename = f"{MEDIA_ROOT}/ec_files/{faculty.email.split('@')[0]}_{course.code}.csv"

                # Participation report for given course
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                    
                    # File header
                    writer.writerow(
                        ['fsu_id', 'last_name', 'first_name', 'questions_answered', 'team_division', 'role'])
                    
                    for student in students:
                        if student.profile.fsu_id is None:
                            fsu_id = 'none'
                        else:
                            fsu_id = student.profile.fsu_id

                        if student.profile.team is None:
                            questions_answered = 'none'
                        else:
                            questions_answered = student.profile.team.questions_answered        

                        writer.writerow([
                            fsu_id,
                            student.last_name,
                            student.first_name,
                            questions_answered,
                            student.profile.team.get_division_code(),
                            student.profile.get_role()
                        ])
    
    logger.info(
        f'Processed extra credit files for {num_courses} courses')


@shared_task
def email_faculty(domain):
    faculty_members = Faculty.objects.all()
    fpath = f"{MEDIA_ROOT}/ec_files/"
    message_subject = 'Programming Contest EC files'
    messages = []

    for faculty in faculty_members:
        found_files = False

        # Detemine if EC files exist for given faculty member
        for fname in os.listdir(fpath):
            uid = faculty.email.split('@')[0]
            if uid in fname:
                found_files = True
                break

        if found_files:
            message = render_to_string('contestadmin/ec_available_email.html', {
                'faculty': faculty,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(uid)),
            })
        else:
            message = render_to_string('contestadmin/no_ec_available_email.html', {
                'faculty': faculty,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(uid)),
            })

        messages.append((
            message_subject,
            message,
            DEFAULT_FROM_EMAIL,
            [faculty.email]
        ))

    messages = tuple(messages)  # Group messages for mass mailing
    try:
        send_mass_mail(messages, fail_silently=False)
    except:
        logger.error("Failed to send extra credit notification to faculty.")


@shared_task
@transaction.atomic
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
                    team.questions_answered = row[3]
                    team.score = row[4]
                    team.save()
                    num_teams += 1
                except:
                    logger.error(f'Could not process contest results for team {id}')
            else:
                pass

    logger.info(f'Processed contest results for {num_teams} teams')


@shared_task
def clear_discord_channel(id):
    try:
        webhook = Webhook.from_url(
            BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    except InvalidArgument:
        logger.error('Failed to connect to bot channel webhook.')
    else:
        message = '$clear '+str(id)
        # Executing webhook.
        webhook.send(content=message)


@shared_task
def create_discord_lfg_roles():
    try:
        webhook = Webhook.from_url(
            BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    except InvalidArgument:
        logger.error('Failed to connect to bot channel webhook.')
    else:
        message = '$create_roles'
        # Executing webhook.
        webhook.send(content=message)


@shared_task
def remove_all_discord_lfg_roles():
    try:
        webhook = Webhook.from_url(
            BOT_CHANNEL_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    except InvalidArgument:
        logger.error('Failed to connect to bot channel webhook.')
    else:
        message = '$remove_all_roles'
        # Executing webhook.
        webhook.send(content=message)
